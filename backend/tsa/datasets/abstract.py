from abc import abstractmethod
from typing import Generator

from tsa import typing


class FramesDataset:
    @property
    @abstractmethod
    def frames(self) -> Generator[typing.NP_FRAME, None, None]:
        pass
