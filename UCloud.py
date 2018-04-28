#!/usr/bin/env python
# -*- coding: utf-8 -*-
from actions.uhost import DescribeUHostTags, UHost
from actions.ulb import ULB
from actions.eip import EIP
from actions.sms import SendSms
from actions.region import GetRegion
from client import UcloudApiClient
from addict import Dict
from collections import defaultdict


class UCloudZone:

    def __init__(self, public_key, private_key):
        self.public_key, self.private_key = public_key, private_key
        self.client = UcloudApiClient(public_key=self.public_key, private_key=self.private_key)
        self.info = Dict()
        self.region = None
        self.id = None
        self.init_region()

    def set(self, zone_id):
        if zone_id in self.info:
            self.id = zone_id
            self.region = self.info[zone_id]
        else:
            raise KeyError

    def init_region(self):
        for info in [Dict(info) for info in self.client.get(GetRegion())]:
            if info.IsDefault:
                self.region = info.Region
                self.id = info.Zone
            self.info[info['Zone']] = info['Region']

    def items(self):
        return self.info.items()

    def __repr__(self):
        return f'<{self.__class__.__name__}(Zone={self.id}, Region={self.region})>'


class UCloud:

    def __init__(self, public_key, private_key):
        self.public_key, self.private_key = public_key, private_key
        self.zone = UCloudZone(public_key, private_key)
        self.client = UcloudApiClient(public_key=self.public_key, private_key=self.private_key)
        self.hosts = defaultdict(list)
        self.uhost = UHost(self)
        self.ulb = ULB(self)
        self.eip = EIP(self)

    def send_sms(self, phone, context):
        action = SendSms(phone, context)
        self.client.get(action)

    @property
    def tags(self):
        action = DescribeUHostTags(zone_id=self.zone.id, region_id=self.zone.region)
        return [Dict(i) for i in self.client.get(action)]

    def switch_zone(self, zone_id):
        self.zone.set(zone_id)


