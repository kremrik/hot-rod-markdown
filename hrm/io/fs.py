from typing import Generator, Union


__all__ = ["read_file", "write_file"]


def read_file(path: str) -> Generator[str, None, None]:
    with open(path, "r") as f:
        for line in f:
            yield line


def write_file(
    path, data: Union[str, Generator[str, None, None]]
) -> None:
    with open(path, "w") as f:
        if isinstance(data, str):
            f.write(data)
        else:
            for line in data:
                f.write(line)
