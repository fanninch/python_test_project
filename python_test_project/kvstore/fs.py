from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

from .base import BaseStoreImpl
from .errors import KeyNotFound


def _key_to_path(root: Path, key: str) -> Path:
    # Keep key-as-path semantics but prevent directory escapes.
    p = Path(*key.split("/"))
    p = p.with_suffix(p.suffix or ".bin")
    full = (root / p).resolve()
    root_resolved = root.resolve()
    if not str(full).startswith(str(root_resolved)):
        raise ValueError("Key escapes root directory")
    return full


class FileSystemStoreImpl(BaseStoreImpl):
    """
    Implementation of a file system-based storage backend.

    This class provides a concrete implementation of a storage backend that uses
    a file system for persisting data. Data is stored in a hierarchical directory
    structure where each key is mapped to a corresponding file.

    :ivar _root: The root directory where all data will be stored. This attribute
                 defines the base path for key-file mappings.
    :type _root: pathlib.Path
    """
    def __init__(self, root_dir: str) -> None:
        super().__init__()
        self._root = Path(root_dir)
        self._root.mkdir(parents=True, exist_ok=True)

    def _get_impl(self, key: str) -> bytes:
        path = _key_to_path(self._root, key)
        if not path.exists():
            raise KeyNotFound(key)
        return path.read_bytes()

    def _set_impl(self, key: str, value: bytes, *, ttl: int | None) -> None:
        path = _key_to_path(self._root, key)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_bytes(value)
        os.replace(tmp, path)  # atomic on POSIX

    def _delete_impl(self, key: str) -> bool:
        path = _key_to_path(self._root, key)
        try:
            path.unlink()
            return True
        except FileNotFoundError:
            return False

    def _list_impl(self, prefix: str) -> Iterable[str]:
        # Walk the root and yield keys that match the prefix
        for p in self._root.rglob("*"):
            if p.is_file():
                rel = p.relative_to(self._root).as_posix()
                # strip .bin if present (to mirror get/set behavior)
                if rel.endswith(".bin"):
                    rel = rel[:-4]
                if rel.startswith(prefix):
                    yield rel