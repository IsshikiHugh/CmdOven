import sys
from typing import Callable

from oven.oven import Oven, build_oven

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

def get_arg() -> str:
    return ' '.join(sys.argv[1:])


def cli_log() -> None:
    return notify(get_arg())


def cli_cmd() -> None:
    return oven.ding_cmd(get_arg())