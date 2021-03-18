from os import rename, remove
from os.path import basename, dirname, join, exists
from typing import Generator, Union


__all__ = ["read_file", "write_file"]


def read_file(path: str) -> Generator[str, None, None]:
    with open(path, "r") as f:
        for line in f:
            yield line


def write_file(
    path, data: Union[str, Generator[str, None, None]]
) -> None:
    tmp_path = tmp_file(path)

    try:
        with open(tmp_path, "w") as f:
            if isinstance(data, str):
                f.write(data)
            else:
                for line in data:
                    f.write(line)
        rename(tmp_path, path)

    except Exception as e:
        print(e)
        if exists(tmp_path):
            remove(tmp_path)
        raise


def tmp_file(path: str) -> str:
    file_name = basename(path)
    file_dir = dirname(path)
    temp_name = f".{file_name}.tmp"
    temp_path = join(file_dir, temp_name)
    return temp_path
