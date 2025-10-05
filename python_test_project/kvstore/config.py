from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Backend = Literal["memory", "fs"]

@dataclass(frozen=True, slots=True)
class StoreConfig:
    """
    Represents the configuration for a data store.

    This class encapsulates the details required to configure and
    manage a store. It allows specifying the backend storage type,
    the root directory for data storage, and an optional default
    time-to-live (TTL) for stored items.

    :ivar backend: The backend storage mechanism to be used.
    :type backend: Backend
    :ivar root_dir: The root directory for data storage, or None if
        not applicable.
    :type root_dir: str | None
    :ivar default_ttl: The default TTL (in seconds) for stored
        items, or None if no default TTL is to be applied.
    :type default_ttl: int | None
    """
    backend: Backend
    root_dir: str | None = None
    default_ttl: int | None = None
