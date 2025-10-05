from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Iterable

from .api import KeyValueStore
from .errors import InvalidKey

_KEY_PATTERN = re.compile(r"^[A-Za-z0-9._:/-]{1,256}$")


class BaseStoreImpl(ABC, KeyValueStore):
    """
    Base class for implementing key-value storage backends.

    This class provides a common interface and validation logic for
    key-value store operations such as get, set, delete, and list.
    It enforces key validation and delegates the actual storage
    operations to subclass-specific implementations.

    :ivar attribute1: Description of the first attribute of the class (if any).
    :type attribute1: type
    :ivar attribute2: Description of the second attribute of the class (if any).
    :type attribute2: type
    """
    def __init__(self) -> None:
        """Initialize the base store."""
        # Place shared state here if needed (metrics, logging, etc.)

    # ---- public API with validation -> delegate to protected hooks ----

    def get(self, key: str) -> bytes:
        self._validate_key(key)
        return self._get_impl(key)

    def set(self, key: str, value: bytes, *, ttl: int | None = None) -> None:
        self._validate_key(key)
        self._set_impl(key, value, ttl=ttl)

    def delete(self, key: str) -> bool:
        self._validate_key(key)
        return self._delete_impl(key)

    def list(self, prefix: str = "") -> Iterable[str]:
        if prefix and not _KEY_PATTERN.match(prefix):
            raise InvalidKey(f"Invalid prefix: {prefix!r}")
        return self._list_impl(prefix)

    def close(self) -> None:
        """Release resources (override in subclasses if needed)."""
        return None

    # ---- subclass hooks ----

    @abstractmethod
    def _get_impl(self, key: str) -> bytes: ...

    @abstractmethod
    def _set_impl(self, key: str, value: bytes, *, ttl: int | None) -> None: ...

    @abstractmethod
    def _delete_impl(self, key: str) -> bool: ...

    @abstractmethod
    def _list_impl(self, prefix: str) -> Iterable[str]: ...

    # ---- helpers ----

    @staticmethod
    def _validate_key(key: str) -> None:
        if not _KEY_PATTERN.match(key):
            raise InvalidKey(
                "Keys must match /^[A-Za-z0-9._:/-]{1,256}$/; got %r" % key
            )
