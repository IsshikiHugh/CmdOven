import json
from typing import Dict, Tuple
import base64
import hashlib
import hmac
from datetime import datetime

import requests

from oven.backends.api import NotifierBackendBase, RespStatus
from oven.consts import REQ_TIMEOUT
from .info import FeishuExpInfo, FeishuLogInfo


class FeishuBackend(NotifierBackendBase):
    def __init__(self, cfg: Dict):
        # Validate the configuration.
        assert (
            'hook' in cfg and '<?>' not in cfg['hook']
        ), 'Please ensure the validity of "feishu.hook" field in the configuration file!'
        assert (
            'signature' in cfg and '<?>' not in cfg['signature']
        ), 'Please ensure the validity of "feishu.signature" field in the configuration file!'

        # Setup.
        self.cfg = cfg
        self.url = cfg['hook']
        self.secret = cfg['signature']

    def _gen_sign(self, secret):
        timestamp = int(datetime.now().timestamp())
        string_to_sign = f'{timestamp}\n{secret}'
        hmac_code = hmac.new(
            string_to_sign.encode('utf-8'), digestmod=hashlib.sha256
        ).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return sign

    def notify(self, info: FeishuExpInfo):
        """
        Ask the bot to send raw string message.
        Check docs: https://www.feishu.cn/hc/zh-CN/category/7177281426289704962-%E9%A3%9E%E4%B9%A6%E6%9C%BA%E5%99%A8%E4%BA%BA%E5%8A%A9%E6%89%8B
        """

        # 1. Prepare data dict.
        sign = self._gen_sign(self.secret)
        timestamp = int(datetime.now().timestamp())

        formatted_data = {
            'timestamp': timestamp,
            'sign': sign,
            'msg_type': 'interactive',
            'card': info.format_information(),
        }
        # 2. Post request and get response.
        has_err, err_msg = False, ''
        try:
            resp = requests.post(
                self.url, json=formatted_data, timeout=REQ_TIMEOUT
            )
            resp_dict = json.loads(resp.text)
            has_err, err_msg = self._parse_resp(resp_dict)
        except Exception as e:
            has_err = True
            err_msg = f'Cannot send message to Feishu: {e}'

        # 3. Return response dict.
        resp_status = RespStatus(has_err=has_err, err_msg=err_msg)
        return resp_status

    def get_meta(self) -> Dict:
        """Generate meta information for information object."""
        return {
            'host': self.cfg.get('host', None),
            'signature': self.cfg.get('signature', None),
            'backend': 'FeishuBackend',
        }

    # ================ #
    # Utils functions. #
    # ================ #

    def _parse_resp(self, resp_dict) -> Tuple[bool, str]:
        """
        Reference: https://open.feishu.cn/community/articles/7298688341381546012
        Addition: according to test, if the message is sent successfully, the response will have `code=0`.
        """
        has_err, err_msg = False, ''
        if 'code' in resp_dict and resp_dict['code'] != 0:
            code = resp_dict['code']
            msg = resp_dict['msg']
            has_err, err_msg = True, f'[{code}] {msg}'
        return has_err, err_msg
