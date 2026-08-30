from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ExtractionRequest(BaseModel):
    """Validates input message for JSON extraction."""

    model_config = ConfigDict(str_strip_whitespace=True)

    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Text to extract user information from",
    )


class User(BaseModel):
    """Extracted user information."""

    name: str = Field(..., min_length=1, description="User's name")
    email: Optional[EmailStr] = Field(None, description="Email Address")
    age: Optional[float] = Field(None, ge=0, le=100, description="Age in years")
