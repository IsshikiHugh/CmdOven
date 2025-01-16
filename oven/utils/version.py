import re
import requests

from typing import Tuple


def get_latest_oven_version() -> str:
    from oven.consts import oven_version_url
    src = requests.get(oven_version_url).text
    # Match __version__ = 'x.x.x' and return 'x.x.x'
    matches = re.search(r'__version__\s*=\s*[\'\"](.+)[\'\"]', src)
    if matches is None:
        version = 'Missing!'
    else:
        version = matches.group(1)
    return version


def version_x_lt_y(x, y) -> bool:
    ''' It only supports version with digits. Won't be used temporarily. '''
    def version_to_tuple(version) -> Tuple:
        return tuple(map(int, version.split('.')))
    return version_to_tuple(x) < version_to_tuple(y)