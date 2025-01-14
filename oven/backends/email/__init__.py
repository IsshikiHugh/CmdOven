import json
import requests
from typing import Union, Dict
import base64
import hashlib
import hmac
from datetime import datetime
from oven.backends.api import NotifierBackendBase, RespStatus
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .info import EmailExpInfo, EmailLogInfo

class EmailBackend(NotifierBackendBase):
    
    def __init__(self, cfg:Dict):
        # Validate the configuration.
        assert 'smtp_server' in cfg, \
            'Please ensure the validity of "email.smtp_server" field in the configuration file!'
        assert 'smtp_port' in cfg and isinstance(cfg['smtp_port'],int), \
            'Please ensure the validity of "email.smtp_port" field in the configuration file!'
        assert 'sender_email' in cfg, \
            'Please ensure the validity of "email.sender_email" field in the configuration file!'
        assert 'sender_pwd' in cfg, \
            'Please ensure the validity of "email.sender_pwd" field in the configuration file!'
        assert 'receiver_email' in cfg, \
            'Please ensure the validity of "email.receiver_email" field in the configuration file!'

        
        # Setup.
        self.cfg = cfg
        self.smtp_server = cfg['smtp_server']
        self.smtp_port = cfg['smtp_port']
        self.sender_email = cfg['sender_email']
        self.sender_pwd = cfg['sender_pwd']
        self.receiver_email = cfg['receiver_email']
    

    def get_meta(self) -> Dict:
        ''' Generate meta information for information object. '''
        return {
            'smtp_server': self.cfg.get('smtp_server', None),
            'smtp_port': self.cfg.get('smtp_port', None),
            'sender_email': self.cfg.get('sender_email', None),
            'sender_pwd': self.cfg.get('sender_pwd', None),
            'receiver_email': self.cfg.get('receiver_email', None),
        }
        
    def notify(self, info:EmailExpInfo):
        '''
        Sending email to notify
        '''

        # 1. Prepare data dict.
        timestamp = int(datetime.now().timestamp())

        formatted_data = {
                "timestamp": timestamp,
                # "sign": sign,
                "msg_type": "mail",
                "card": info.format_information(),
        }
        # mail config
        smtp_server = self.cfg['smtp_server']
        smtp_port = self.cfg['smtp_port']
        sender_email = self.cfg['sender_email']
        sender_password = self.cfg['sender_pwd']
        receiver_email = self.cfg['receiver_email']

        subject = formatted_data['card']['subject']
        body = formatted_data['card']['body']

        # Initilaize the message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Attach body
        msg.attach(MIMEText(body, 'plain'))
        has_err = False
        try:
            # Connect to the SMTP server.
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # TLS encryption
            server.login(sender_email, sender_password)  # login
            # Sending
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
        except Exception as e:
            has_err = True
            # meta = ...
            # after RespStatus is implemented

        # 3. Return response dict.
        resp_status = RespStatus(has_err=True, meta={})  # TODO: fill in the response status, since its not implemented, 'has_err' is always True.
        return resp_status
