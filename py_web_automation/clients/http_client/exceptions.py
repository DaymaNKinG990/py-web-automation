from ...exceptions import WebAutomationError


class ValidationError(WebAutomationError):
    """
    Exception raised for data validation errors.

    Raised when input data validation fails or data format is invalid.

    Example:
        >>> raise ValidationError("Invalid URL format", "URL must start with http:// or https://")
    """

    pass
