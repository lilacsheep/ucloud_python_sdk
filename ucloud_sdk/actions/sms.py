#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ucloud_sdk.actions.base import BaseAction


class SendSms(BaseAction):
    name = 'SendSms'
    response = 'RetCode'

    def __init__(self, phone, context):
        super(SendSms, self).__init__()
        self.phone = phone
        self.set_params('Content', context)
        self.make_phone()

    def make_phone(self):
        if isinstance(self.phone, str):
            self.phone = self.phone.split(',')
        if isinstance(self.phone, list):
            for index, phone in enumerate(self.phone):
                self.set_params(f'Phone.{index}', phone)
