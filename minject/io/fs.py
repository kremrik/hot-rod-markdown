from typing import Iterable


__all__ = ["read_file", "write_file"]


def read_file(path: str) -> Iterable[str]:
    with open(path, "r") as f:
        return f.readlines()


def write_file(path, data: str) -> None:
    with open(path, "w") as f:
        f.write(data)
