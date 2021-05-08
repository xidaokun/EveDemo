import datetime
import hashlib
import base64
import requests
import json


class RongYun(object):
    base_url = 'https://app.cloopen.com:8883'

    def __init__(self, accountSid, accountToken, appId, templateId):
        self.accountSid = accountSid
        self.accountToken = accountToken
        self.appId = appId
        self.templateId = templateId

    def get_request_url(self, sig):
        return self.base_url \
                   + '/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s'%(self.accountSid, sig)

    def get_timestamp(self):
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def get_signature(self, timestamp):
        data = self.accountSid + self.accountToken + timestamp
        md = hashlib.md5()
        md.update(data.encode())
        return md.hexdigest().upper()

    def get_request_header(self, timestamp):
        data = self.accountSid + ':' + timestamp
        auth = base64.b64encode(data.encode()).decode()
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': auth
        }

    def get_request_body(self, phone, code):
        return {
            "to": phone,
            "appId": self.appId,
            "templateId": self.templateId,
            "datas": [code, "3"],
        }

    def request_api(self, url, header, body):
        res = requests.post(url, headers=header, data=body)
        return res.text

    def run(self, phone, code):
        timestamp = self.get_timestamp()
        sig = self.get_signature(timestamp)
        url = self.get_request_url(sig)
        header = self.get_request_header(timestamp)
        body = self.get_request_body(phone, code)
        data = self.request_api(url, header, json.dumps(body))
        return data
