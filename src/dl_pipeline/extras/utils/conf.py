from pathlib import Path

from kedro.config import OmegaConfigLoader
from kedro.framework.project import settings

from dl_pipeline.extras.utils.kedro import KedroVariables


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent.parent.parent


def _get_nested_value(d, key_path):
    if d is None:
        return None

    keys = key_path.split(".")
    if len(keys) == 1:
        return d.get(keys[0])
    return _get_nested_value(d[keys[0]], ".".join(keys[1:]))


def get_params(key_path=None):
    """
    通过key_path获取参数 (形式如 a.b.c)
    为 None 时返回所有参数
    """
    try:
        context = KedroVariables().context
        params = context.params
    except AttributeError:
        project_root = get_project_root()
        conf_path = str(project_root / settings.CONF_SOURCE)
        conf_loader = OmegaConfigLoader(conf_source=conf_path, env="local")
        params = conf_loader["parameters"]
    if key_path is None:
        return params
    else:
        return _get_nested_value(params, key_path)


def get_credentials(key_path=None):
    """
    通过key_path获取参数 (形式如 a.b.c)
    为 None 时返回所有参数
    """
    try:
        context = KedroVariables().context
        credentials = context._get_config_credentials()
    except AttributeError:
        project_root = get_project_root()
        conf_path = str(project_root / settings.CONF_SOURCE)
        conf_loader = OmegaConfigLoader(conf_source=conf_path, env="local")
        credentials = conf_loader["credentials"]
    if key_path is None:
        return credentials
    else:
        return _get_nested_value(credentials, key_path)
