from pathlib import Path

from lightning.pytorch.loggers import TensorBoardLogger


class Logger(TensorBoardLogger):
    def __init__(self, save_dir: Path = "logs", default_hp_metric: bool = False):
        super().__init__(save_dir, default_hp_metric=default_hp_metric)
