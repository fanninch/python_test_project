class KeyNotFound(KeyError):
    """Raised when a key is not present in the store."""


class InvalidKey(ValueError):
    """Raised when a key is syntactically invalid for the backend."""


class Misconfiguration(RuntimeError):
    """Raised when a config is missing required fields for a backend."""
