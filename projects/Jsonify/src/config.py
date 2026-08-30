"""Configuration for Jsonify extraction."""

import os
from dataclasses import dataclass


@dataclass
class ExtractionConfig:
    """Configuration for JSON extraction."""

    model: str = os.getenv("JSONIFY_MODEL", "llama3.2")
    temperature: float = float(os.getenv("JSONIFY_TEMPERATURE", "0"))
    max_retries: int = int(os.getenv("JSONIFY_MAX_RETRIES", "4"))
    retry_min_wait: int = int(os.getenv("JSONIFY_RETRY_MIN_WAIT", "1"))
    retry_max_wait: int = int(os.getenv("JSONIFY_RETRY_MAX_WAIT", "8"))
    timeout: float = float(os.getenv("JSONIFY_TIMEOUT", "60"))

    @property
    def extraction_prompt(self) -> str:
        """System prompt for extraction."""
        return """You are a JSON extraction engine. Given text, extract all mentioned fields into valid JSON format.
                  Fields to extract: name, email, age.
                  Only output valid JSON, no prose or explanations."""


config = ExtractionConfig()
