from abc import ABC, abstractmethod

import lightning as L


class CustomDataModule(L.LightningDataModule, ABC):
    def __init__(self):
        super().__init__()

    def prepare_data(self):
        pass

    @abstractmethod
    def setup(self, stage: str = None):
        pass

    @abstractmethod
    def train_dataloader(self):
        pass

    @abstractmethod
    def val_dataloader(self):
        pass

    @abstractmethod
    def test_dataloader(self):
        pass
