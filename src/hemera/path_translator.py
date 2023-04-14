import json
from absl import logging
import os.path
from pathlib import Path

OS_ENV_NAME = "HEMERA_PATHS"
DEFAULT_PATH = "~/.hemera_paths"
_PATHS = None


def load_paths(path: Path | str = None, path_dict: dict[str, Path | str] = None):
    """
    Load path dict, if you have set up the config correctly this should happen automatically and so no need to call this
    Can be helpful if you want to reload paths, add paths etc.
    :param path:
    :param path_dict:
    :return:
    """
    global _PATHS
    if _PATHS is not None:
        logging.warning("`load_paths` called with an existing path dict already loaded")

    if path_dict is not None:
        _PATHS = path_dict
        return

    path = os.getenv(OS_ENV_NAME, DEFAULT_PATH) if path is None else path
    path = Path(path).expanduser()

    if not path.exists():
        logging.warning("No path dict found at: %s", path)
        return

    logging.info("attempting to load path dict from: %s", path)
    with open(path) as f:
        load_file = json.load(f)
        _PATHS = load_file


load_paths()


def get_path(folder: str, default_base: str = ".") -> Path:
    """
    Gets the local path for the project folder
    if none exists, the path maps to `default_base / folder`
    :param folder:
    :param default_base:
    :return: Path object
    """
    path = _PATHS[folder] if folder in _PATHS else os.path.join(default_base, folder)
    return Path(path)
