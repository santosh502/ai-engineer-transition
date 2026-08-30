"""Tests for JSON extraction functionality."""

from unittest.mock import patch

import pytest
from src.core.extractor import extract_json_from_response
from src.core.models import ExtractionRequest, User
from src.utils.exceptions import ExtractionError


class TestExtractJsonFromResponse:
    """Test the JSON extraction strategies."""

    def test_strategy_1_raw_json(self):
        """Test Strategy 1: Extract pure JSON (no markdown)."""
        response = '{"name": "John", "email": "john@example.com", "age": 30}'

        result = extract_json_from_response(response)

        assert result == {"name": "John", "email": "john@example.com", "age": 30}

    def test_strategy_2_markdown_json(self):
        # ARRANGE - LLM returns JSON in markdown
        response = """Here's the extracted data:

        ```json
        {"name": "Alice", "email": "alice@example.com", "age": 28}
        ```

        Let me know if you need more info."""

        result = extract_json_from_response(response)

        assert result == {"name": "Alice", "email": "alice@example.com", "age": 28}

    def test_strategy_3_json_buried_in_text(self):
        """Test Strategy 3: Extract JSON buried in explanation text."""
        response = """Based on the input, here's what I found:

                  The person's details are: {"name": "Bob", "email": "bob@example.com", "age": 45}

                    Hope this helps!"""

        result = extract_json_from_response(response)

        assert result == {"name": "Bob", "email": "bob@example.com", "age": 45}

    def test_empty_response_raises_error(self):
        """Test that empty response raises ExtractionError."""
        response = ""

        with pytest.raises(ExtractionError):
            extract_json_from_response(response)

    def test_whitespace_only_raises_error(self):
        """Test that whitespace-only response raises error."""
        # ARRANGE
        response = "   \n\t  "

        with pytest.raises(ExtractionError):
            extract_json_from_response(response)

    def test_invalid_json_raises_error(self):
        # ARRANGE - Text with no JSON at all
        response = "Sorry, I cannot find that information"

        with pytest.raises(ExtractionError):
            extract_json_from_response(response)


class TestExtractJsonFunctionErrorHandling:
    """Test error handling in extract_json function."""

    def test_malformed_ollama_response_structure(self):
        """Test graceful handling of unexpected response structure."""
        with patch("ollama.chat") as mock_chat:
            # Missing 'message' key
            mock_chat.return_value = {"error": "Something went wrong"}

            with pytest.raises(Exception):  # Will eventually raise after retries
                from src.core.extractor import extract_json

                extract_json("test message")

    def test_ollama_response_missing_content(self):
        """Test when message structure exists but no content key."""
        with patch("ollama.chat") as mock_chat:
            mock_chat.return_value = {"message": {}}  # Missing 'content' key

            with pytest.raises(Exception):  # Will eventually raise after retries
                from src.core.extractor import extract_json

                extract_json("test message")


class TestExtractionRequest:
    """Test input validation with Pydantic."""

    def test_valid_message(self):
        """Test that valid message is accepted."""
        # ARRANGE
        message = "My name is John and I'm 30 years old"

        request = ExtractionRequest(message=message)

        assert request.message == message

    def test_message_stripped_of_whitespace(self):
        """Test that whitespace is automatically stripped."""
        message = "   John Doe   "

        request = ExtractionRequest(message=message)

        assert request.message == "John Doe"

    def test_empty_message_rejected(self):
        """Test that empty message is rejected."""
        message = ""

        with pytest.raises(ValueError):
            ExtractionRequest(message=message)

    def test_message_too_long_rejected(self):
        """Test that message exceeding max length is rejected."""
        message = "a" * 5000  # Exceeds max of 4000

        with pytest.raises(ValueError):
            ExtractionRequest(message=message)


class TestUserModel:
    """Test User schema validation."""

    def test_valid_user_creation(self):
        """Test creating valid user."""
        user = User(name="John", email="john@example.com", age=30)

        assert user.name == "John"
        assert user.email == "john@example.com"
        assert user.age == 30

    def test_user_with_optional_fields(self):
        """Test user with optional fields (email and age can be None)."""
        user = User(name="Jane")

        assert user.name == "Jane"
        assert user.email is None
        assert user.age is None

    def test_user_with_empty_name_rejected(self):
        """Test that empty name is rejected."""
        with pytest.raises(ValueError):
            User(name="")
