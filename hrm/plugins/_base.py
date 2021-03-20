from hrm.io import fs
from hrm.logger import logger

from abc import ABC, abstractmethod
from os import chdir
from os.path import dirname
from typing import Generator, Union


LOGGER = logger(__file__)


class HotRodMarkdown(ABC):
    __help__: str
    __doc__: str

    def __init__(self, path: str) -> None:
        self.path = path
        self._directory = ""

    @property
    def directory(self) -> str:
        if not self._directory:
            self._directory = dirname(self.path)
        return self._directory

    @abstractmethod
    def transform(
        self,
        md_contents: Generator[str, None, None],
        **kwargs,
    ) -> Union[str, Generator[str, None, None]]:
        pass

    def run(self, **kwargs) -> None:
        self._chdir()

        md_contents = self._read()
        xform_results = self.transform(
            md_contents, **kwargs
        )

        if not xform_results:
            LOGGER.info("No changes to write")
            return

        self._write(xform_results)

    def _chdir(self) -> None:
        LOGGER.info(f"Setting pwd to {self.directory}")
        chdir(self.directory)

    def _read(self) -> Generator[str, None, None]:
        LOGGER.info(f"Reading {self.path}")
        return fs.read_file(self.path)

    def _write(
        self, data: Union[Generator[str, None, None], str]
    ) -> None:
        LOGGER.info(f"Writing {self.path}")
        fs.write_file(path=self.path, data=data)
