class MediaGeneratorError(Exception):
    """Base exception for the media generator."""


class ConfigError(MediaGeneratorError):
    """Raised when required configuration is missing."""


class ApiError(MediaGeneratorError):
    """Raised when the configured provider returns an error."""
