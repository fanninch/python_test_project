from __future__ import annotations

from .api import KeyValueStore
from .config import StoreConfig
from .errors import Misconfiguration
from .inmem import InMemoryStoreImpl
from .fs import FileSystemStoreImpl

def create_store(cfg: StoreConfig) -> KeyValueStore:
    """
    Creates a key-value store instance based on the provided configuration.

    This function initializes a specific implementation of a key-value store
    depending on the backend specified in the configuration. Supported backends
    are in-memory and file system-based implementations. If an unsupported
    backend is provided or required parameters for a backend are missing, an
    error will be raised.

    :param cfg: Configuration object for the store containing backend type and
        related parameters.
    :type cfg: StoreConfig
    :return: An instance of the specified key-value store implementation.
    :rtype: KeyValueStore
    :raises Misconfiguration: If required parameters are missing or the backend
        type is not recognized.
    """
    if cfg.backend == "memory":
        return InMemoryStoreImpl(default_ttl=cfg.default_ttl)
    if cfg.backend == "fs":
        if not cfg.root_dir:
            raise Misconfiguration("root_dir is required for backend='fs'")
        return FileSystemStoreImpl(cfg.root_dir)
    raise Misconfiguration(f"Unknown backend: {cfg.backend!r}")
