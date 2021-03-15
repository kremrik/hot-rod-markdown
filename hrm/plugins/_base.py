from hrm.io import fs

from abc import ABC, abstractmethod
from os import chdir
from os.path import dirname
from typing import Iterable, Optional


class HotRodMarkdown(ABC):
    __help__: str

    def __init__(self, path: str, verbose: bool) -> None:
        self.path = path
        self.verbose = verbose
        self._directory = ""

    @property
    def directory(self) -> str:
        if not self._directory:
            self._directory = dirname(self.path)
        return self._directory

    @abstractmethod
    def transform(
        self, md_contents: Iterable[str]
    ) -> Optional[str]:
        pass

    def run(self) -> None:
        self._chdir()

        md_contents = self._read()
        xform_results = self.transform(md_contents)

        if not xform_results:
            return

        self._write(xform_results)

        if self.verbose:
            print(f"Changed: {self.path}")

    def _chdir(self) -> None:
        chdir(self.directory)

    def _read(self) -> Iterable[str]:
        return fs.read_file(self.path)

    def _write(self, data: str) -> None:
        fs.write_file(path=self.path, data=data)
