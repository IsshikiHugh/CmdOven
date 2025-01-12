import time
from oven.backends.api.info import LogInfoBase, Signal
from oven.backends.dingtalk.info import DingTalkExpInfo, DingTalkLogInfo, lines2reply, plain2md

line_split = '\n'


class LarkExpInfo(DingTalkExpInfo):

    def format_information(self) -> str:
        information = []
        information.append([{
            'tag': 'text',
            'text': self.exp_info
        }])
        if len(self.aux_info) > 0:
            information.append([{
                'tag': 'text',
                'text': self.aux_info
            }])
        if len(self.current_description) > 0:
            information.append([{
                'tag': 'text',
                'text': self.current_description
            }])
        return information

    def custom_signal_handler(self) -> None:
        # Initialization.
        if self.current_signal == Signal.I:
            self.exp_meta_info = self._init_meta()
            # Update the meta information to member variables.
            self.host = self.exp_meta_info['host']
            self.cmd = self.exp_meta_info['cmd']
            self.sec_key = self.exp_meta_info['sec_key']
            return

        # Format the time anyway.
        self.readable_time = time.strftime('%a %d %b %Y %I:%M:%S %p %Z', time.localtime(self.current_timestamp))

        # Format the information for later use.
        self.current_description = plain2md(self.current_description)
        if self.current_signal == Signal.S:
            if len(self.current_description) == 0:
                self.exp_info = f'🔥 {self.cmd}'
            else:
                self.exp_info = f'🔥 {self.cmd}\n' + '\n'.join(self.current_description.split('\n'))
            self.exp_info_backup = self.exp_info
            self.aux_info = ''
        else:
            self.exp_info = '\n'.join(self.exp_info_backup.split('\n'))

            cost_info = f'⏱️ Time Cost: {str(self.current_timestamp - self.start_timestamp)}s.'
            if self.current_signal == Signal.P:
                status_info = f'🏃 Running!'
            elif self.current_signal == Signal.E:
                status_info = f'❌ Error!'
            elif self.current_signal == Signal.T:
                status_info = f'🔔 Done!'
            else:
                assert False, f'Unknown signal: {self.current_signal}'

            self.aux_info = cost_info + line_split + status_info

    def get_title(self) -> str:
        ''' The title is necessary for Feishu markdown message. '''
        return f'{self.readable_time} @ {self.host}'


class LarkLogInfo(DingTalkLogInfo, LarkExpInfo):

    def format_information(self) -> str:
        # 1. Format meta information and time.
        information = []
        information.append([{
            'tag': 'text',
            'text': self.current_description
        }])
        return information