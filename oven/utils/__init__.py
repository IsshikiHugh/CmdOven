import os
from typing import Union
from pathlib import Path

from .cfg import get_cfg_temp, modify_cfg_with_new_backend


def get_home_path() -> Path:
    home_path = None
    if 'OVEN_HOME' in os.environ:
        home_path = Path(os.environ['OVEN_HOME'])
    else:
        from oven.consts import default_cfg_home
        home_path = Path(default_cfg_home)
    return home_path


def get_cfg_path() -> Path:
    return get_home_path() / 'cfg.yaml'


def dump_cfg_temp(overwrite:bool=False) -> Union[str, Path]:
    ''' Download the config template according to latest configuration schema. '''
    path = get_cfg_path()

    if not overwrite and Path(path).exists():
        print(f'File already exists: {path}')
    else:
        print(f'Dumping config template to: {path}')
        with open(path, 'w') as f:
            f.write(get_cfg_temp())
    return path


def toggle_backend(backend:str) -> None:
    cfg_fn = get_cfg_path()
    modify_cfg_with_new_backend(cfg_fn, backend)
    return None


def print_manual() -> None:
    manual_path = __file__.replace('__init__.py', 'manual.txt')
    with open(manual_path, 'r') as f:
        manual = f.read()
    return print(manual)


def error_redirect_to_manual(action) -> None:
    print(f'😢 Action`{action}` is invalid!')
    return print_manual()