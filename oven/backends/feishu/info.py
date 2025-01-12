import time
from typing import Union, Dict

from oven.backends.api import Signal, ExpInfoBase, LogInfoBase


class FeishuExpInfo(ExpInfoBase):

    # ================ #
    # Pre-defined API. #
    # ================ #

    def format_information(self) -> dict:
        information = {
            "title": f'{self.readable_time} @ {self.host}',
            "content": [
                [{
                    "tag": "text",
                    "text": self.exp_info
                }],
                [{
                    "tag": "text",
                    "text": self.aux_info
                }],
                [{
                    "tag": "text",
                    "text": self.current_description
                }]
            ]
        }
        return information


    def custom_signal_handler(self) -> None:
        # Initialization.
        if self.current_signal == Signal.I:
            self.exp_meta_info = self._init_meta()
            # Update the meta information to member variables.
            self.host = self.exp_meta_info['host']
            self.cmd = self.exp_meta_info['cmd']
            self.signature = self.exp_meta_info['signature']
            return

        # Format the time anyway.
        self.readable_time = time.strftime('%a %d %b %Y %I:%M:%S %p %Z', time.localtime(self.current_timestamp))

        # Format the information for later use.
        self.current_description = self.current_description
        if self.current_signal == Signal.S:
            self.exp_info = f'🔥 `{self.cmd}`\n\n' + (self.current_description)
            self.exp_info_backup = self.exp_info
            self.aux_info = ''
        else:
            self.exp_info = self.exp_info_backup

            cost_info = f'⏱️ **Time Cost**: {str(self.current_timestamp - self.start_timestamp)}s.'
            if self.current_signal == Signal.P:
                status_info = f'🏃 **Running!**'
            elif self.current_signal == Signal.E:
                status_info = f'❌ **Error!**'
            elif self.current_signal == Signal.T:
                status_info = f'🔔 Done!'
            else:
                assert False, f'Unknown signal: {self.current_signal}'

            self.aux_info = "\n".join([cost_info, status_info])



    # =================== #
    # Customized methods. #
    # =================== #

    # ================ #
    # Utils functions. #
    # ================ #

    def _init_meta(self) -> Dict:
        # The host name of the machine where the experiment is running.
        default_host = self.exp_meta_info['default_host']
        custom_host = self.exp_meta_info.get('host', None)
        if custom_host is None:
            host = default_host
        else:
            host = f'{custom_host}({default_host})'
        host = host.strip()
        # Return the validated meta information.
        validated_meta = {
            'host': host,
            'cmd': self.exp_meta_info['cmd'],
            'signature': self.exp_meta_info['signature'],
        }
        return validated_meta


class FeishuLogInfo(LogInfoBase, FeishuExpInfo):

    # ================ #
    # Pre-defined API. #
    # ================ #

    def format_information(self) -> dict:
        information = {
            "title": f'{self.readable_time} @ {self.host}',
            "content": [
                [{
                    "tag": "text",
                    "text": self.current_description
                }],
            ]
        }
        return information
    
    def custom_signal_handler(self) -> None:
        # Initialization.
        if self.current_signal == Signal.I:
            self.exp_meta_info = self._init_meta()
            # Update the meta information to member variables.
            self.host = self.exp_meta_info['host']
            self.signature = self.exp_meta_info['signature']
            return

        # Format the time anyway.
        self.readable_time = time.strftime('%a %d %b %Y %I:%M:%S %p %Z', time.localtime(self.current_timestamp))
