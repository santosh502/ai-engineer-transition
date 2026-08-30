import json
import logging
import re

import ollama
from src.config import config
from src.core.models import ExtractionRequest, User
from src.utils.exceptions import ExtractionError, PermanentError, RetryableError
from src.utils.retry import retry_extraction

try:
    from httpx import TimeoutException
except ImportError:
    TimeoutException = Exception

logger = logging.getLogger(__name__)


def extract_json_from_response(content: str) -> dict:
    """Extract JSON from LLM response using multiple strategies.

    Strategies (in order):
    1. Try raw JSON parsing (LLM returned pure JSON)
    2. Extract from markdown code blocks (```json...```)
    3. Find first { and last } (JSON buried in text)

    Args:
        content: Raw response from LLM

    Returns:
        Parsed JSON dict

    Raises:
        ExtractionError: If JSON cannot be extracted or parsed
    """
    if not content or not content.strip():
        raise ExtractionError("LLM returned empty response")

    content = content.strip()

    # Strategy 1: Try raw JSON parsing
    try:
        data = json.loads(content)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    # Strategy 2: Extract from markdown code blocks
    json_match = re.search(r"```(?:json)?\s*(.*?)\s*```", content, re.DOTALL)
    if json_match:
        try:
            json_str = json_match.group(1).strip()
            data = json.loads(json_str)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass

    # Strategy 3: Find first { and last } (JSON buried in explanation)
    brace_start = content.find("{")
    brace_end = content.rfind("}")
    if brace_start != -1 and brace_end != -1 and brace_end > brace_start:
        try:
            json_str = content[brace_start : brace_end + 1]
            data = json.loads(json_str)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass

    # All strategies failed
    raise ExtractionError("Could not extract valid JSON from LLM response")


@retry_extraction
def extract_json(message: str) -> User:
    """Extract structured JSON from unstructured text using LLM.

    Args:
        message: Unstructured text containing user information

    Returns:
        Validated User object

    Raises:
        ExtractionError: If extraction or validation fails
    """
    try:
        # Validate input with Pydantic
        request = ExtractionRequest(message=message)
        message = request.message

        client = ollama.Client(timeout=config.timeout)
        response = client.chat(
            model=config.model,
            messages=[
                {"role": "system", "content": config.extraction_prompt},
                {
                    "role": "user",
                    "content": f"Extract user details from this message: {message}",
                },
            ],
            options={"temperature": config.temperature},
        )

        try:
            content = response["message"]["content"].strip()
        except (KeyError, TypeError) as e:
            logger.error(f"Invalid response structure from LLM: {e}")
            raise RetryableError(f"Invalid LLM response structure: {e}")

        # Validate output is not empty
        if not content:
            raise ExtractionError("LLM returned empty response")

        # Extract JSON using multiple strategies
        data = extract_json_from_response(content)

        # Validate schema with Pydantic
        return User(**data)

    except TimeoutException as e:
        logger.error(f"Request timed out after {config.timeout}s: {e}")
        raise RetryableError(
            f"Request timed out (limit: {config.timeout}s) - retrying..."
        )
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing failed: {e}")
        raise RetryableError(f"Invalid JSON in response: {e}")
    except ValueError as e:
        logger.error(f"Validation failed: {e}")
        raise PermanentError(f"Validation failed: {e}")
    except ExtractionError as e:
        logger.error(f"JSON extraction failed: {e}")
        raise RetryableError(f"Could not extract JSON: {e}")
    except (RetryableError, PermanentError):
        raise
    except Exception as e:
        logger.error(f"Unexpected error during extraction: {e}")
        raise RetryableError(f"Unexpected error: {e}")
