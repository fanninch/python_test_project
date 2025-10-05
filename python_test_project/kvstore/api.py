from __future__ import annotations

from typing import Protocol, runtime_checkable, Iterable

@runtime_checkable
class KeyValueStore(Protocol):
    """
    Defines a protocol for a key-value store with standard operations like get, set,
    delete, list, and close. This protocol can be implemented to create various types
    of key-value stores, offering flexibility in storage backends while maintaining
    a common interface.

    The interface supports retrieval, storage, and deletion of key-value pairs,
    optional setting of expiration time (TTL) for keys, listing keys by prefix,
    and proper resource management via the close method.
    """
    def get(self, key: str) -> bytes: ...
    def set(self, key: str, value: bytes, *, ttl: int | None = None) -> None: ...
    def delete(self, key: str) -> bool: ...
    def list(self, prefix: str = "") -> Iterable[str]: ...
    def close(self) -> None: ...
