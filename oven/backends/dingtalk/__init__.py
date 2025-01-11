import json
import requests
from typing import Union, Dict

from oven.backends.api import NotifierBackendBase, RespStatus

from .info import DingTalkExpInfo, DingTalkLogInfo


class DingTalkBackend(NotifierBackendBase):

    def __init__(self, cfg:Dict):
        # Validate the configuration.
        assert 'hook' in cfg and 'access_token=<?>' not in cfg['hook'], \
            'Please ensure the validity of "dingtalk.hook" field in the configuration file!'
        assert 'secure_key' in cfg and '<?>' not in cfg['secure_key'], \
            'Please ensure the validity of "dingtalk.secure_key" field in the configuration file!'

        # Setup.
        self.cfg = cfg
        self.url = cfg['hook']

    def notify(self, info:DingTalkExpInfo):
        '''
        Ask the bot to send raw string message.
        Check docs: https://open.dingtalk.com/document/orgapp/custom-bot-send-message-type#6f14e4d007kju
        '''

        # 1. Prepare data dict.
        data = {
            'markdown':{
                # When comment on this message, title will be shown in quotation.
                'title': info.get_title(),
                # The things shown directly in the message.
                'text': info.format_information(),
            },
            'msgtype': 'markdown',
        }

        # 2. Post request and get response.
        try:
            resp = requests.post(self.url, json=data)
            resp_dict = json.loads(resp.text)
        except:
            resp_dict = {}

        # 3. Return response dict.
        resp_status = RespStatus(has_err=True, meta={})  # TODO: fill in the response status, since its not implemented, 'has_err' is always True.
        return resp_status


    def get_meta(self) -> Dict:
        ''' Generate meta information for information object. '''
        return {
            'host': self.cfg.get('host', None),
            'sec_key': self.cfg['secure_key'],
            'backend': 'DingTalkBackend'
        }