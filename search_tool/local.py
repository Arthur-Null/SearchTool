import json
import yaml
import os
from typing import Callable, Any, Union
from pathlib import Path
from itertools import product

from .util import get_search_space, get_config

loader = yaml.SafeLoader


def get_full_config(config: dict, dir_name: Path):
    while "base" in config:
        base_config = os.path.normpath(os.path.join(dir_name, config.pop("base")))
        dir_name = os.path.dirname(base_config)
        with open(base_config, "r") as f:
            try:
                base_config = yaml.load(f, Loader=loader)
            except Exception:
                base_config = json.load(f)
        base_config.update(config)
        config = base_config
    return config


def run_exps(config: Union[dict, str, Path], run: Callable[[dict], Any]):
    """Run an experiment or a set of experiments.

    Args:
        config: The path to config.
        run: The function to run a single experiment.
    """
    if type(config) == dict:
        config_path = "."
    elif type(config) == str:
        config_path = os.path.normpath(config)
        with open(config, "r") as f:
            if config.endswith(".json"):
                config = json.load(f)
            else:
                config = yaml.load(f, Loader=loader)
    elif type(config) == Path:
        config_path = os.path.normpath(config)
        with open(config, "r") as f:
            if config.suffix == ".json":
                config = json.load(f)
            else:
                config = yaml.load(f, Loader=loader)
    log_dir = config.pop("log_dir")
    search_space = config.pop("search")

    keys = []
    spaces = []
    for k, v in search_space.items():
        keys.append(k)
        spaces.append(get_search_space(v))
    config_list = []
    for paras in product(*spaces):
        tmp_config = get_config(keys, paras, config)
        if tmp_config in config_list:
            continue
        else:
            config_list.append(tmp_config)
    for index in range(len(config_list)):
        config_list[index]["log_dir"] = f"{log_dir}/{index}/"

    for c in config_list:
        full_config = get_full_config(c, config_path)
        run(full_config)
