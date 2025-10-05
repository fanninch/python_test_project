from typing import Protocol, runtime_checkable, Iterable, TypeVar, Generic, Optional

T = TypeVar("T")


@runtime_checkable
class Repository(Protocol, Generic[T]):

    def get(self, key: str) -> T: ...
    def add(self, item: T, *, key: Optional[str] = None) -> str: ...


class InMemoryRepo(Repository[T], Generic[T]):
    def __init__(self) -> None:
        self._store: dict[str, T] = {}

    def get(self, key: str) -> T:
        return self._store[key]

    def add(self, item: T, *, key: Optional[str] = None) -> str:
        k = key or str(len(self._store))
        self._store[k] = item
        return k

if __name__ == "__main__":

    repo: Repository[int] = InMemoryRepo[int]()
    assert isinstance(repo, Repository)
