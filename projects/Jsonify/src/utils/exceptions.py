class ExtractionError(Exception):
    """Raised when the model output isn't usable JSON or fails validation."""

    pass


class ValidationError(Exception):
    """Raised when the input or output data fails validation."""

    pass


class PermanentError(Exception):
    """Raised when a permanent error occurs that should not be retried."""

    pass


class RetryableError(Exception):
    """Raised when a retryable error occurs that may succeed on retry."""

    pass
