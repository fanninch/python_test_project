
"""
kvstore package

A minimal, educational key–value store with interchangeable backends. This
package demonstrates a clean, modular package layout where a thin public API is
exposed from __init__.py while concrete implementations live in submodules.

What this module exports
- KeyValueStore: a typing.Protocol describing the store interface (get/set/delete/list/close)
- StoreConfig: a small dataclass used to configure a store (backend, root_dir, default_ttl)
- Errors: KeyNotFound, InvalidKey, Misconfiguration
- create_store: a factory that returns a store instance based on StoreConfig

Backends available
- "memory": in‑process, volatile store
- "fs": file‑system backed store (requires a root_dir)

Example

.. code-block:: python

    from python_test_project.kvstore import (
        create_store, StoreConfig, KeyNotFound
    )

    # In-memory store
    store = create_store(StoreConfig(backend="memory"))
    store.set("greeting", b"hello")
    print(store.get("greeting").decode())  # -> "hello"

    # Listing keys
    for k in store.list():
        print("key:", k)

    # Handling missing keys
    try:
        store.get("missing")
    except KeyNotFound:
        print("not found")

    # File-system store (data persisted under ./data)
    fs_store = create_store(StoreConfig(backend="fs", root_dir="./data"))
    fs_store.set("answer", b"42")
    fs_store.close()

Purpose of the kvstore package
- Serve as a teaching/PoC example of how to structure a small package with a
  clear public surface, swappable implementations, and a simple factory.
- Not intended for production use.
"""
from .api import KeyValueStore
from .config import StoreConfig
from .errors import KeyNotFound, InvalidKey, Misconfiguration
from .factory import create_store

__all__ = [
    "KeyValueStore",
    "StoreConfig",
    "KeyNotFound",
    "InvalidKey",
    "Misconfiguration",
    "create_store",
]
