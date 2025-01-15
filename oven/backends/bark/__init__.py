import json
import requests
from typing import Union, Dict
import base64
import hashlib
import hmac
from datetime import datetime
from oven.backends.api import NotifierBackendBase, RespStatus

from .info import BarkExpInfo, BarkLogInfo


class BarkBackend(NotifierBackendBase):

    def __init__(self, cfg:Dict):
        # Validate the configuration.
        assert 'device_token' in cfg and '<?>' not in cfg['device_token'], \
            'Please ensure the validity of "bark.device_token" field in the configuration file!'
        assert 'level' in cfg and cfg['level'] in ['active', 'timeSensitive', 'passive', 'critical'], \
            'Please ensure the validity of "bark.level" field in the configuration file!'
        assert 'group' in cfg and '<?>' not in cfg['group'], \
            'Please ensure the validity of "bark.group" field in the configuration file!'
        assert 'url' in cfg , \
            'Please ensure the validity of "bark.url" field in the configuration file!'

        # Setup.
        self.cfg = cfg
        self.device_token = cfg['device_token']
        self.url = "https://api.day.app/" + self.device_token 
        self.icon = "" # TODO: add icon support.

    def _gen_sign(self, secret):
        timestamp = int(datetime.now().timestamp())
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return sign


    def notify(self, info:BarkExpInfo):
        '''
        bark the message.
        Check docs: https://bark.day.app/#/?id=bark
        '''
        # 1. Prepare data dict.
        formatted_data = info.format_information()
        
        payload = {
            "title": formatted_data["title"],
            "subtitle": formatted_data["subtitle"],
            "body": formatted_data["content"],
            "group": self.cfg['group'],
            "icon" : self.icon,
            "url": self.cfg['url']
        }
        if '<?>' in self.cfg['url']: payload.pop('url')
        # 2. Post request and get response.
        try:
            resp = requests.post(self.url, json=payload)
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
            'signature': self.cfg.get('signature', None),
            'backend': 'BarkBackend'
        }
