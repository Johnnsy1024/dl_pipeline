import lightning as L
from lightning.pytorch.callbacks import RichProgressBar


class Trainer(L.Trainer):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.callbacks = [RichProgressBar(leave=True)]
