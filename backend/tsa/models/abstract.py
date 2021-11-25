from abc import abstractmethod

from tsa.datasets.abstract import FramesDataset


class PredictableModel:
    @abstractmethod
    def predict(self, dataset: FramesDataset):
        pass
