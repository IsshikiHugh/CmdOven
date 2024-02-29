import os
import sys
import json
import requests
from omegaconf import OmegaConf

class DingNotifier():
    def __init__(self, hook:str, secure_key=None, host=None, *args, **kwargs):
        self.url     = hook # Web URL gotten from DingTalk like {API url}?access_token={token}
        self.sec_key = secure_key # Secure key word gotten from DingTalk.
        if host is None:
            self.host = ''
        else:
            self.host = f'@ {host}'

    def _error_handler(self, resp_dict:dict):
        '''
        TODO: a lot of error to be handling.
        '''
        if 'errcode' in resp_dict.keys() and 'errmsg'in resp_dict.keys() :
            errcode = resp_dict['errcode']
            errmsg = resp_dict['errmsg']
            if errcode != 0:
                print(f'[CmdOven-ERROR] request error with {errcode} - {errmsg}')
        else:
            print(f'[CmdOven-ERROR] request error with illegal response: {resp_dict}')

    def send_str(self, msg:str):
        '''
        Ask the bot to send raw string message.
        Check docs: https://open.dingtalk.com/document/orgapp/custom-bot-send-message-type#6f14e4d007kju
        '''
        # 1. Prepare info message.
        time = os.popen('date').read().strip()
        prefix = f'###### {time} {self.host}\n\n'
        
        # 1. Prepare data dict.
        data = {
            'markdown':{
                'title': self.sec_key,
                'text': prefix + msg
            },
            'msgtype': 'markdown',
        }

        # 2. Post request and get response.
        try:
            resp = requests.post(self.url, json=data)
            resp_dict = json.loads(resp.text)
        except:
            resp_dict = {}
        self._error_handler(resp_dict)

        # 3. Return response dict.
        return resp_dict

def build_notifier_from_cfg(cfg_path:str):
    ''' Build DingNotifier from config file. '''
    cfg = OmegaConf.load(cfg_path)
    return DingNotifier(**cfg)

def build_notifier_from_env(): 
    ''' Build DingNotifier from env var. '''
    hook    : str = os.getenv('CMD_OVEN_HOOK')      # You should get the full web hook of ding's bot manager.
    sec_key : str = os.getenv('CMD_OVEN_SEC_KEY')   # We use secure word to avoid illegal request.
    host    : str = os.getenv('CMD_OVEN_HOST')      # Optional, use this to distinguish different machine.
    if hook is None or not hook.startswith('https://oapi.dingtalk.com/robot/send?access_token='):
        raise ValueError(f'[DingNotify-ERROR] Invalid hook environment variable: $CMD_OVEN_HOOK = {hook}')
    if not len(sec_key) > 0:
        raise ValueError(f'[DingNotify-ERROR] Security key not set! $CMD_OVEN_SEC_KEY is empty!')
    return DingNotifier(hook, sec_key, host)

def lines2reply(lines):
    ''' It changes lines to string block and add quotation mark at the beginning of each line.'''
    return '> ' + '\n>\n> '.join(lines)

if __name__ == '__main__':
    notifier = build_notifier_from_cfg('./config.yaml')
    # notifier = build_notifier_from_env()

    # START ding!
    cmd = ' '.join(sys.argv[1:])
    prefix_s = os.popen('date').read().strip()
    start_msg_lines = []
    start_msg_lines.append(f'🔥 Action **start** with command:')
    start_msg_lines.append(f'💡 `{cmd}`')
    start_msg = '\n\n'.join(start_msg_lines)
    notifier.send_str(start_msg)
    
    # run the command
    os.system(cmd)

    # FINISH ding!
    reply_prefix = lines2reply(start_msg_lines)
    finish_msg_lines = [reply_prefix]
    finish_msg_lines.append(f'🔔 Action **finished**!')
    finish_msg = '\n\n'.join(finish_msg_lines)
    notifier.send_str(finish_msg)