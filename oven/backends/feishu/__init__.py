import json
import requests
from typing import Union, Dict
import base64
import hashlib
import hmac
from datetime import datetime
from oven.backends.api import NotifierBackendBase, RespStatus

from .info import FeishuExpInfo, FeishuLogInfo


class FeishuBackend(NotifierBackendBase):

    def __init__(self, cfg:Dict):
        # Validate the configuration.
        assert 'hook' in cfg and 'access_token=<?>' not in cfg['hook'], \
            'Please ensure the validity of "feishu.hook" field in the configuration file!'
        assert 'secure_key' in cfg and '<?>' not in cfg['secure_key'], \
            'Please ensure the validity of "feishu.secure_key" field in the configuration file!'

        # Setup.
        self.cfg = cfg
        self.url = cfg['hook']
        self.secret = cfg['secure_key']

    def _gen_sign(self, secret):
        timestamp = int(datetime.now().timestamp())
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        hmac_code = hmac.new(
            string_to_sign.encode("utf-8"), digestmod=hashlib.sha256
        ).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return sign
    
    
    def notify(self, info:FeishuExpInfo):
        '''
        Ask the bot to send raw string message.
        Check docs: https://www.feishu.cn/hc/zh-CN/category/7177281426289704962-%E9%A3%9E%E4%B9%A6%E6%9C%BA%E5%99%A8%E4%BA%BA%E5%8A%A9%E6%89%8B
        '''

        # 1. Prepare data dict.
        sign = self._gen_sign(self.secret)
        timestamp = int(datetime.now().timestamp())

        formatted_data = {
            "timestamp": timestamp,
            "sign": sign,
            "msg_type": "post",
            "content": {
                "post": {
                    "en_us": info.format_information(),
                }
            }
        }
        # 2. Post request and get response.
        try:
            resp = requests.post(self.url, json=formatted_data)
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
            'backend': 'FeishuBackend'
        }
