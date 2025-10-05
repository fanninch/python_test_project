from __future__ import annotations

import time
from typing import Iterable

from .base import BaseStoreImpl
from .errors import KeyNotFound

class InMemoryStoreImpl(BaseStoreImpl):
    """
    Implementation of an in-memory key-value store with optional TTL (time-to-live).

    This class provides a lightweight in-memory storage solution with support for
    expiration of keys. It is well-suited for temporary caching or storing ephemeral
    data during the runtime of an application. The keys are stored with optional
    expiration times, and expired keys are automatically pruned during access.

    :ivar default_ttl: The default time-to-live for keys in the store, in seconds.
        If None, keys do not expire unless a specific TTL is provided during key
        insertion.
    :type default_ttl: int | None
    """
    def __init__(self, *, default_ttl: int | None = None) -> None:
        super().__init__()
        # key -> (value, expires_at | None)
        self._data: dict[str, tuple[bytes, float | None]] = {}
        self._default_ttl = default_ttl

    def _now(self) -> float:
        return time.monotonic()

    def _get_impl(self, key: str) -> bytes:
        try:
            value, expires = self._data[key]
        except KeyError as exc:
            raise KeyNotFound(key) from exc

        if expires is not None and self._now() >= expires:
            # Expired: delete and signal not found
            del self._data[key]
            raise KeyNotFound(key)
        return value

    def _set_impl(self, key: str, value: bytes, *, ttl: int | None) -> None:
        use_ttl = ttl if ttl is not None else self._default_ttl
        expires_at = self._now() + use_ttl if use_ttl else None
        self._data[key] = (value, expires_at)

    def _delete_impl(self, key: str) -> bool:
        return self._data.pop(key, None) is not None

    def _list_impl(self, prefix: str) -> Iterable[str]:
        now = self._now()
        # Prune expired lazily and yield keys with the prefix
        to_delete: list[str] = []
        for k, (_, exp) in self._data.items():
            if exp is not None and now >= exp:
                to_delete.append(k)
                continue
            if k.startswith(prefix):
                yield k
        for k in to_delete:
            self._data.pop(k, None)