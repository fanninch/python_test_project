# Python Test Project

Purpose
- This repository provides simple, concrete examples of Python package structures and serves as a sandbox for proof-of-concept (PoC) work. It is intentionally lightweight to make it easy to explore layout, imports, and basic packaging patterns.

What’s included
- A minimal package: `python_test_project/`
  - `kvstore/`: a toy key–value store demonstrating package structure, modular design, and interchangeable backends
    - Backends: in-memory and filesystem
    - Supporting modules: API, base classes, factory, config, and error types
  - Example scripts:
    - `kvstore_example.py`: shows how to use the kvstore API
    - `main.py`: entry-point style script you can run directly

Quick start
1) Ensure you have Python 3.11+ installed.
2) From the project root, you can run the examples:
   - Run the main script:
     - `python -m python_test_project.main`
   - Run the kvstore example:
     - `python -m python_test_project.kvstore_example`

Repository goals
- Demonstrate clean, readable package organization
- Provide a safe place to try PoC ideas without production constraints
- Offer small, testable components you can extend or replace

Notes
- Requires Python 3.11+; examples may use 3.11 features (e.g., typing improvements and stdlib additions).
- This project is not intended for production use; it is for learning and experimentation.
- Feel free to copy patterns you find useful into your own projects.


## kvstore package

A small, educational key–value store that showcases a clean, modular package layout with interchangeable backends. The public API is kept thin and is re-exported from the package’s __init__.py, while concrete implementations live in submodules.

Layout at a glance
- python_test_project/kvstore/
  - __init__.py: exposes the public API (KeyValueStore, StoreConfig, errors, create_store)
  - api.py: defines the KeyValueStore Protocol (get/set/delete/list/close)
  - base.py: optional shared helpers/base types for implementations
  - factory.py: create_store(cfg) builds the correct backend from configuration
  - config.py: StoreConfig dataclass (backend, root_dir, default_ttl)
  - errors.py: error types (KeyNotFound, InvalidKey, Misconfiguration)
  - inmem.py: in‑process, volatile backend
  - fs.py: filesystem-backed backend

Why this layout is useful
- Clear public surface: users import from python_test_project.kvstore instead of reaching into internals.
- Swappable backends: implementations live behind a stable Protocol and factory.
- Testable and extensible: each backend is isolated, making it easy to add or swap new ones.
- Separation of concerns: API, config, errors, factory, and implementations are decoupled.

Example usage (same as in the package docstring)
```python
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
```
