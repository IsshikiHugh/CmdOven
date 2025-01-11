import sys
from typing import Callable

from oven.oven import Oven, build_oven
from oven.utils import (
    dump_cfg_temp,
    get_home_path,
    print_manual,
    error_redirect_to_manual,
)

# Global oven.
oven:Oven = build_oven()


# =================================== #
# Utils functions for in-package use. #
# =================================== #

def monitor(func) -> Callable:
    '''
    Notifier decorator for a function. 

    Usage:
    ```
    @oven.monitor
    def foo() -> None:
        ...
    ```
    It's equivalent to:
    ```
    @oven.bake
    def foo() -> None:
        ...
    ```
    '''
    global oven
    return oven.ding_func(func)


def notify(msg:str) -> None:
    '''
    Notify a single message logging.

    Usage:
    ```
    @oven.notify('Hello World!')
    ```
    It's equivalent to:
    ```
    @oven.ding('Hello World!')
    ```
    '''
    global oven
    return oven.ding_log(msg)


# 🍟 Interesting alias just for fun, these alias are aligned with CLI.
bake = monitor  # @oven.bake = @oven.monitor
ding = notify   # oven.ding(...) = oven.notify(...)


# =============================== #
# CLI utils for command line use. #
# =============================== #

def cli_log() -> None:
    ''' CLI command `ding`. '''
    log = ' '.join(sys.argv[1:])
    return notify(log)


def cli_cmd() -> None:
    ''' CLI command `bake`. '''
    cmd = ' '.join(sys.argv[1:])
    return oven.ding_cmd(cmd)


def cli_full() -> None:
    ''' CLI command `oven`. '''
    action = sys.argv[1]
    args = sys.argv[2:]

    if action == 'help':
        return print_manual()
    elif action == 'ding':
        return notify(' '.join(args))
    elif action == 'bake':
        return oven.ding_cmd(' '.join(args))
    elif action == 'init-cfg':
        return dump_cfg_temp(overwrite=False)
    elif action == 'reset-cfg':
        return dump_cfg_temp(overwrite=True)
    elif action == 'home':
        return print(get_home_path())
    else:
        return error_redirect_to_manual(action)