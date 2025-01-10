from typing import Union, Dict

from .info import *


class RespStatus:
    def __init__(self, has_err:bool, meta:Dict):
        self.has_err:bool = has_err
        self.meta:Dict = meta


class NotifierBackendBase:

    # ========================================== #
    # Functions below should/can be overwritten. #
    # ========================================== #


    def __init__(self, cfg:Dict) -> None:
        ''' Read necessary information from config file. '''
        pass


    def notify(self, info:ExpInfoBase) -> RespStatus:
        raise NotImplementedError


    def get_meta(self) -> Dict:
        ''' Generate meta information for information object. '''
        raise NotImplementedError