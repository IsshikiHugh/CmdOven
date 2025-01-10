import os
import traceback
import subprocess
from typing import Type, Callable, Any, List, Union
from pathlib import Path
from omegaconf import OmegaConf
from oven.backends.api import NotifierBackendBase, ExpInfoBase, LogInfoBase, Signal

class Oven:
    def __init__(self, cfg) -> None:
        self.cfg = cfg

        # Register some important classes.
        self.ExpInfoClass:Type[ExpInfoBase]
        self.LogInfoClass:Type[LogInfoBase]
        self.backend:NotifierBackendBase
        self._init_notifier()


    def ding_log(self, msg:str) -> None:
        ''' Notify a single log information. '''
        meta = self.backend.get_meta()
        log_info = self.LogInfoClass(self.backend, exp_meta_info=meta, description=msg)


    def ding_func(self, func:Callable) -> Callable:
        ''' Function decorator to notify the experiment information. '''
        def inner(*args, **kwargs) -> Any:
            # Generate function information.
            n_args = len(args)
            n_kwargs = len(kwargs.keys())
            args_info = ''
            if n_args > 0:
                args_info += f', #args={n_args}'
            if n_kwargs > 0:
                args_info += f', #kwargs={n_kwargs}'
                kwargs_keys = list(kwargs.keys())
                if n_kwargs <= 5:
                    kwargs_keys = ', '.join(kwargs_keys)
                    args_info += f', kwargs={kwargs_keys} )'
                else:
                    kwargs_keys = ', '.join(kwargs_keys[:5])
                    args_info += f', kwargs={kwargs_keys}...'
            if len(args_info) > 2:
                args_info = args_info[2:]

            # Start the experiment.
            meta = self.backend.get_meta()
            meta['cmd'] = f'{func.__name__}({args_info})'
            exp_info = self.ExpInfoClass(backend=self.backend, exp_meta_info=meta)

            try:
                # Running the experiment.
                resp = func(*args, **kwargs)
            except Exception as e:
                # Finish baking with error.
                exp_info.update_signal(signal=Signal.E, description=f'Function internal exception detected: {e}')
                raise e

            # Experiment finished.
            exp_info.update_signal(signal=Signal.T)
            return resp
        return inner


    def ding_cmd(self, cmd:str) -> None:
        ''' Run a command and notify before & after the command. '''
        meta = self.backend.get_meta()
        meta['cmd'] = cmd.strip()
        exp_info = self.ExpInfoClass(backend=self.backend, exp_meta_info=meta)

        try:
            # run command, then capture output and error.
            subprocess.run(cmd, shell=True, check=True, encoding='utf-8')
        except subprocess.CalledProcessError as e:
            # Finish baking with error.
            exp_info.update_signal(signal=Signal.E, description=f'Command error detected: {e}')
            raise e

        # Experiment finished.
        exp_info.update_signal(signal=Signal.T)


    def _init_notifier(self) -> None:
        ''' Initialize the notifier. '''
        # 1. Through useless things.
        backend = self.cfg.backend
        self.cfg = self.cfg[backend]
        self.cfg['backend'] = backend
        if backend == 'dingtalk':
            from oven.backends.dingtalk import DingtalkBackend, DingtalkExpInfo, DingtalkLogInfo
            self.ExpInfoClass = DingtalkExpInfo
            self.LogInfoClass = DingtalkLogInfo
            self.backend = DingtalkBackend(self.cfg)
        else:
            self.ExpInfoClass = ...
            self.LogInfoClass = ...
            self.backend = ...
            raise NotImplementedError(f'Notifier backend `{backend}` is not supported yet.')



default_cfg_path = Path.home() / '.config' / 'oven' / 'cfg.yaml'
def build_oven(cfg_path:Union[Path, str]=None, raise_err:bool=False) -> Oven:
    # 1. Search if Oven configuration path is defined environment variable.
    env_cfg_path = None
    if 'OVEN_HOME' in os.environ:
        env_cfg_path = Path(os.environ['OVEN_HOME']) / 'cfg.yaml'
        cfg_path = env_cfg_path
    else:
        cfg_path = default_cfg_path

    # 2. Load config.
    oven = None

    try:
        if not Path(cfg_path).exists():
            raise FileNotFoundError(f'Oven configuration file not found at `{cfg_path}`.')
        cfg = OmegaConf.load(cfg_path)
        oven = Oven(cfg)
    except Exception as e:
        # Generate tips.
        searched_paths = f'\n- {cfg_path}'
        print(f'Oven configuration file not found or invalid. Searched paths: {searched_paths}')
        print(f'You are suggested to set the environment variable `OVEN_HOME` to the directory containing the `cfg.yaml`, or ensure the validity of config files mentioned.')

        traceback.print_exc()
        if raise_err:
            raise e
    return oven

oven = build_oven()


