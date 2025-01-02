import copy
from pathlib import PurePosixPath
from typing import Any, Dict

import pandas as pd
import urllib3
from kedro.io.core import get_filepath_str
from kedro_datasets.pandas import SQLQueryDataset
from sqlalchemy import create_engine
from sqlalchemy.exc import NoSuchModuleError

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class UnverifiedSQLQueryDataSet(SQLQueryDataset):
    @classmethod
    def create_connection(cls, connection_str: str, connection_args: dict) -> None:
        """Given a connection string, create singleton connection
        to be used across all instances of ``SQLTableDataSet`` that
        need to connect to the same source.
        """
        if connection_str in cls.engines:
            return

        try:
            engine = create_engine(connection_str, connect_args={"verify": False})
        except ImportError as import_error:
            raise import_error
        except NoSuchModuleError as exc:
            raise exc

        cls.engines[connection_str] = engine

    def _load(self) -> pd.DataFrame:
        load_args = copy.deepcopy(self._load_args)

        if self._filepath:
            load_path = get_filepath_str(PurePosixPath(self._filepath), self._protocol)
            with self._fs.open(load_path, mode="r") as fs_file:
                load_args["sql"] = fs_file.read()

        load_args["sql"] = self._render_sql(load_args["sql"], load_args["render_params"])
        load_args.pop("render_params", None)
        debug = load_args.pop("debug", False)
        if debug:
            print(load_args["sql"])
        return pd.read_sql_query(
            con=self.engine.execution_options(**self._execution_options), **load_args
        )

    def _render_sql(self, sql: str, render_params: dict) -> str:
        """Render SQL template using the render parameters."""
        if render_params:
            # if value in render_params is list or tuple, convert it to tuple
            # to be able to use it in SQL IN clause
            render_params = {
                key: tuple(value) if isinstance(value, (list, tuple)) else value
                for key, value in render_params.items()
            }
            return sql.format(**render_params)
        return sql

    def _describe(self) -> Dict[str, Any]:
        load_args = copy.deepcopy(self._load_args)
        return {
            "sql": str(load_args.pop("sql", None)),
            "filepath": str(self._filepath),
            "load_args": str(load_args),
            "execution_options": str(self._execution_options),
        }
