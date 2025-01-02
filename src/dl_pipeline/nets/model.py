from abc import ABC, abstractmethod

import lightning as L


class CustomModel(L.LightningModuleC, ABC):
    def __init__(self, **kwargs):
        super().__init__()
        self.save_hyperparameters()

    @abstractmethod
    def forward(self, x):
        pass

    @abstractmethod
    def training_step(self, batch, batch_idx):
        pass

    def validation_step(self, batch, batch_idx):
        pass

    def test_step(self, batch, batch_idx):
        pass

    @abstractmethod
    def configure_optimizers(self):
        pass
