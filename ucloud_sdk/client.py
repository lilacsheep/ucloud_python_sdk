#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
from urllib.parse import urljoin
import requests
from requests import exceptions
import json.decoder


class UcloudException(Exception):
    pass


def _verfy_ac(private_key, params: dict):
    items = list(params.items())
    items.sort()

    params_data = "".join([f"{key}{value}" for key, value in items]) + private_key
    hash_new = hashlib.sha1()
    hash_new.update(params_data.encode())
    hash_value = hash_new.hexdigest()
    return hash_value


class UConnection(object):

    def __init__(self):
        self.api_url = 'https://api.ucloud.cn'

    @classmethod
    def send(cls, method, uri, data_or_params: dict):
        _class = cls()
        url = urljoin(_class.api_url, uri)
        if hasattr(_class, method):
            return getattr(_class, method)(url, data_or_params)
        else:
            assert ValueError(f'method not in post or get! Now: {method}')

    def get(self, url, params: dict):
        try:
            response = requests.get(url, params=params)
            data = response.json()
            response.close()
        except (exceptions.ConnectionError, exceptions.ConnectTimeout, json.decoder.JSONDecodeError):
            data = {}
        return data

    def post(self, url, data: dict):
        try:
            response = requests.post(url, data=data)
            data = response.json()
            response.close()
        except (exceptions.ConnectionError, exceptions.ConnectTimeout, json.decoder.JSONDecodeError):
            data = {}
        return data


def _callback(action, response):
    if response['RetCode'] == 0:
        return response[action.response]
    else:
        raise UcloudException(response['Message'])


class UcloudApiClient:

    def __init__(self, public_key, private_key, project_id='org-35793', callback=_callback):
        self.g_params = {'PublicKey': public_key}
        if project_id:
            self.g_params["ProjectId"] = project_id
            self.project_id = project_id
        self.private_key = private_key
        self.conn = UConnection
        self.callback = callback

    def set_project(self, project_id):
        if self.check_projects(project_id):
            self.g_params["ProjectId"] = project_id

    def check_projects(self, project_id):
        for i in self.get_project()['ProjectSet']:
            if i['ProjectId'] == project_id:
                return True
        else:
            return False

    def get_project(self):
        _params = dict(self.cleaned_project_params, Action='GetProjectList')
        _params["Signature"] = _verfy_ac(self.private_key, _params)
        return self.conn.send('get', uri='usub_account', data_or_params=_params)

    @property
    def cleaned_project_params(self):
        _params = self.g_params.copy()
        if 'ProjectId' in _params:
            del _params["ProjectId"]
        return _params

    def get(self, action):
        return self.callback(action, self._send(action))

    def _send(self, action):
        _params = dict(self.g_params if action.need_project else self.cleaned_project_params, **action.params)
        _params["Signature"] = _verfy_ac(self.private_key, _params)
        return self.conn.send(action.method, uri=action.uri, data_or_params=_params)

    @classmethod
    def send(cls, public_key, private_key, action, project_id=None):
        _cls = cls(public_key, private_key, project_id)
        return _cls.callback(action, _cls._send(action))

