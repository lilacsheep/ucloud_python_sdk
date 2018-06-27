#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ucloud_sdk.models.uhost import UHost
from ucloud_sdk.models.ulb import ULB
from ucloud_sdk.models.eip import EIP
from ucloud_sdk.models.umem import UMem
from ucloud_sdk.actions.sms import SendSms
from ucloud_sdk.actions.region import GetRegion
from ucloud_sdk.client import UcloudApiClient
from addict import Dict


class UCloudZone:

    def __init__(self, request):
        self.request = request
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
        for info in [Dict(info) for info in self.request.client.get(GetRegion())]:
            if info.IsDefault:
                self.region = info.Region
                self.id = info.Zone
            self.info[info['Zone']] = info['Region']

    def items(self):
        return self.info.items()

    def __repr__(self):
        return f'<{self.__class__.__name__}(Zone={self.id}, Region={self.region})>'


class UCloud:

    def __init__(self, public_key, private_key, project_id=None):
        self.public_key, self.private_key = public_key, private_key
        self.client = UcloudApiClient(public_key=self.public_key, private_key=self.private_key, project_id=project_id)
        self.zone = UCloudZone(self)
        self.uhost = UHost(self)
        self.ulb = ULB(self)
        self.eip = EIP(self)
        self.umem = UMem(self)

    def send_sms(self, phone, context):
        action = SendSms(phone, context)
        self.client.get(action)

    def switch_project(self, project_id):
        self.client.set_project(project_id)

    def switch_zone(self, zone_id):
        self.zone.set(zone_id)


