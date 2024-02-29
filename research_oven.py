import os
import sys
import json
import requests
# from omegaconf import OmegaConf

class DingNotifier():
    def __init__(self, hook:str, secure_key=None, *args, **kwargs):
        self.url = hook # Web URL gotten from DingTalk like {API url}?access_token={token}
        self.prefix = f'[{secure_key}]' # Secure key word gotten from DingTalk.

    def _error_handler(self, resp_dict:dict):
        '''
        TODO: a lot of error to be handling.
        '''
        if 'errcode' in resp_dict.keys() and 'errmsg'in resp_dict.keys() :
            errcode = resp_dict['errcode']
            errmsg = resp_dict['errmsg']
            if errcode != 0:
                print(f'[ReOven-ERROR] request error with {errcode} - {errmsg}')
        else:
            print(f'[ReOven-ERROR] request error with illegal response: {resp_dict}')

    def send_str(self, msg:str):
        '''
        Ask the bot to send raw string message.
        Check docs: https://open.dingtalk.com/document/orgapp/custom-bot-send-message-type#6f14e4d007kju
        '''
        # 1. Prepare data dict.
        data = {
            'markdown':{
                'title'  : f'{self.prefix}',
                'text': f'{msg}'
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

# def build_notifier_from_cfg(cfg_path:str):
#     ''' Build DingNotifier from config file. '''
#     cfg = OmegaConf.load(cfg_path)
#     return DingNotifier(**cfg)

def build_notifier_from_env(): 
    ''' Build DingNotifier from env var. '''
    hook                     : str = os.getenv('DING_NOTIFIER_HOOK')
    sec_key                  : str = os.getenv('DING_NOTIFIER_SEC_KEY')
    if hook is None or not hook.startswith('https://oapi.dingtalk.com/robot/send?access_token='):
        raise ValueError(f'[DingNotify-ERROR] Invalid hook environment variable: $DING_NOTIFIER_HOOK = {hook}')
    if not len(sec_key) > 0:
        raise ValueError(f'[DingNotify-ERROR] Security key not set! $DING_NOTIFIER_SEC_KEY is empty!')
    return DingNotifier(hook, sec_key)

if __name__ == '__main__':
    # notifier = build_notifier_from_cfg('./config.yaml')
    notifier = build_notifier_from_env()

    # START ding!
    cmd = ' '.join(sys.argv[1:])
    time_s = os.popen('date').read().strip()
    start_msg_lines = []
    start_msg_lines.append(f'###### {time_s}')
    start_msg_lines.append(f'🔥 Action **start** with command:')
    start_msg_lines.append(f'💡 `{cmd}`')
    start_msg = '\n\n'.join(start_msg_lines)
    notifier.send_str(start_msg)
    
    # run the command
    os.system(cmd)

    # FINISH ding!
    time_e = os.popen('date').read().strip()
    reply_prefix = '> ' + '\n>\n> '.join(start_msg_lines)
    finish_msg_lines = [reply_prefix]
    finish_msg_lines.append(f'###### {time_e}')
    finish_msg_lines.append(f'🔔 Action **finished**!')
    finish_msg = '\n\n'.join(finish_msg_lines)
    notifier.send_str(finish_msg)