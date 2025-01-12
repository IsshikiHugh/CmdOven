import json
import requests
from oven.backends.api import RespStatus
from oven.backends.dingtalk import DingTalkBackend
from .info import LarkExpInfo, LarkLogInfo


class LarkBackend(DingTalkBackend):

    def notify(self, info: LarkExpInfo):
        '''
        Ask the bot to send raw string message.
        Check docs: https://open.larkoffice.com/document/client-docs/bot-v3/add-custom-bot
        '''

        # 1. Prepare data dict.
        data = {
            'msg_type': 'post',
            'content': {
                'post': {
                    'zh_cn': {
                        # When comment on this message, title will be shown in quotation.
                        'title': info.get_title(),
                        # The things shown directly in the message.
                        'content': info.format_information(),
                    }
                }
            },
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