import re
from typing import Union
from pathlib import Path

import requests
import omegaconf


def get_cfg_temp() -> str:
    from oven.consts import CFG_TEMP_URL, REQ_TIMEOUT

    return requests.get(CFG_TEMP_URL, timeout=REQ_TIMEOUT).text


def modify_cfg_with_new_backend(
    cfg_path: Union[Path, str], backend: str
) -> bool:
    # 1. Modify the backend field in the configuration file.
    # Directly store omegaconf will destroy the original file structure. Thus, use regex to replace keywords directly in the text.
    cfg_dict = omegaconf.OmegaConf.load(cfg_path)
    with open(cfg_path, 'r') as f:
        cfg_text = f.read()
    old_backend = cfg_dict.backend
    new_backend = backend.lower()

    # Make sure the backend is supported..
    if new_backend not in cfg_dict.keys():
        print(
            f'🙁 Backend "{new_backend}" is not supported right now or not configured. Please check the config file: {cfg_path}'
        )
        return False

    # Match "backend: xxx" and replace "xxx". (There can be multiple spaces between ":" and "xxx".)
    cfg_text = re.sub(
        rf'backend\s*:\s*{old_backend}', f'backend: {new_backend}', cfg_text
    )

    with open(cfg_path, 'w') as f:
        f.write(cfg_text)

    print(f'Backend switched from "{old_backend}" to "{new_backend}".')

    # 2. Check the validity of the backend-specific fields.
    backend_cfg = cfg_dict[new_backend]
    invalid_fields = []
    for k, v in backend_cfg.items():
        if '<?>' in str(v) or v is None:
            invalid_fields.append(k)
    if len(invalid_fields) > 0:
        print(
            f'😾 Backend `{new_backend}` has invalid fields: {invalid_fields}. Please check the config file: {cfg_path}'
        )
        return False

    return True


def get_latest_cfg_version() -> str:
    cfg_temp = get_cfg_temp()
    # Match a line of version : x.x.x and return x.x.x, x can be anything
    matches = re.search(
        r'version\s*:\s*([0-9a-zA-Z-]+\.[0-9a-zA-Z-]+\.[0-9a-zA-Z-]+)',
        cfg_temp,
    )
    if matches is None:
        version = 'Missing!'
    else:
        version = matches.group(1)
    return version
