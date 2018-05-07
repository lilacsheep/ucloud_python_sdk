#!/usr/bin/env python
# -*- coding: utf-8 -*-
from addict import Dict
from ucloud_sdk.exception import EIPNotFound, ShareBandwidthNotFound
from ucloud_sdk.actions.eip import *


class EIPAddress:

    def __init__(self, **kwargs):
        self._attrs = Dict(kwargs)

    @property
    def operator(self):
        return self._attrs.OperatorName

    @property
    def ip(self):
        return self._attrs.IP


class UNetEIPResourceSet:

    def __init__(self, **kwargs):
        self._attrs = Dict(kwargs)

    @property
    def type(self):
        return self._attrs.ResourceType

    @property
    def id(self):
        return self._attrs.ResourceID

    @property
    def name(self):
        return self._attrs.ResourceName

    @property
    def zone(self):
        return self._attrs.Zone


class UNetEIPSet:

    def __init__(self, request, **kwargs):
        self._attrs = Dict(kwargs)
        self.request = request

    @property
    def id(self):
        return self._attrs.EIPId

    @property
    def type(self):
        return self._attrs.BandwidthType

    @property
    def name(self):
        return self._attrs.Name

    @name.setter
    def name(self, name):
        action = UpdateEIPAttribute(self.id)
        action.set_name(name)
        self.request.client.get(action)

    @property
    def tag(self):
        return self._attrs.Tag

    @tag.setter
    def tag(self, tag):
        action = UpdateEIPAttribute(self.id)
        action.set_tag(tag)
        self.request.client.get(action)

    @property
    def remark(self):
        return self._attrs.Remark

    @remark.setter
    def remark(self, remark):
        action = UpdateEIPAttribute(self.id)
        action.set_remark(remark)
        self.request.request.client.get(action)

    @property
    def charge_type(self):
        return self._attrs.ChargeType

    @property
    def status(self):
        return self._attrs.Status

    @property
    def create_time(self):
        return self._attrs.CreateTime

    @property
    def expire_time(self):
        return self._attrs.ExpireTime

    @property
    def eip_address(self):
        return [EIPAddress(**i) for i in self._attrs.EIPAddr]

    @property
    def expire(self):
        return self._attrs.Expire

    @property
    def resource(self):
        return UNetEIPResourceSet(**self._attrs.Resource)

    def release(self):
        action = ReleaseEIP(self.id, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)

    def unbind(self, resource):
        action = UnBindEIP(self.id, resource._type, resource.id, zone_id=self.request.zone.id,
                           region_id=self.request.zone.region)
        self.request.client.get(action)

    def bind(self, resource):
        action = BindEIP(self.id, resource._type, resource.id, zone_id=self.request.zone.id,
                         region_id=self.request.zone.region)
        self.request.client.get(action)


class UNetShareBandwidthSet:

    def __init__(self, request, **kwargs):
        self.request = request
        self._attrs = Dict(kwargs)

    @property
    def id(self):
        return self._attrs.ShareBandwidthId

    @property
    def width(self):
        return self._attrs.ShareBandwidth

    @property
    def charge_type(self):
        return self._attrs.ChargeType

    @property
    def create_time(self):
        return self._attrs.CreateTime

    @property
    def expire_time(self):
        return self._attrs.ExpireTime

    def add_eip(self, ids):
        action = AssociateEIPWithShareBandwidth(self.id, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        action.set_eip_ids(ids)
        return self.request.client.get(action)

    def remove_eip(self, ids):
        action = DisassociateEIPWithShareBandwidth(self.id, band_width=2,
                                                   zone_id=self.request.zone.id, region_id=self.request.zone.region)
        action.set_eip_ids(ids)
        return self.request.client.get(action)

    def new_eip(self, operator_name, charge_type='Month', name=None, tag=None, remark=None):
        action = AllocateEIP(operator_name=operator_name, charge_type=charge_type,
                             zone_id=self.request.zone.id, region_id=self.request.zone.region)
        if name is not None: action.set_name(name)
        if tag is not None: action.set_tag(tag)
        if remark is not None: action.set_remark(remark)
        action.set_share_bandwidth(self.id)
        response = self.request.client.get(action)
        return self.request.eip.get(response[0]['EIPId'])

    @property
    def address(self):
        return [UNetEIPSet(self.request, **i) for i in self._attrs.EIPSet]


class EIP:

    def __init__(self, request):
        self.request = request

    @property
    def instances(self):
        action = DescribeEIP(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return [UNetEIPSet(self.request, **i) for i in self.request.client.get(action)]

    @property
    def unbind_eip(self):
        return [i for i in self.instances if i.status == 'free']

    @property
    def share_bandwidth(self):
        action = DescribeShareBandwidth(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return [UNetShareBandwidthSet(self.request, **i) for i in self.request.client.get(action)]

    def get_share_bandwidth(self, _id) -> UNetShareBandwidthSet:
        for i in self.share_bandwidth:
            if i.id == _id:
                return i
        else:
            raise ShareBandwidthNotFound(_id)

    def get(self, eip_id) -> UNetEIPSet:
        for i in self.instances:
            if i.id == eip_id:
                return i
        else:
            raise EIPNotFound(eip_id)

    def create_eip(self, operator_name, bandwidth=2, charge_type='Month',
                   name=None, tag=None, remark=None, share_bandwidth=None) -> UNetEIPSet:
        action = AllocateEIP(operator_name=operator_name, bandwidth=bandwidth, charge_type=charge_type,
                             zone_id=self.request.zone.id, region_id=self.request.zone.region)
        if name is not None: action.set_name(name)
        if tag is not None: action.set_tag(tag)
        if remark is not None: action.set_remark(remark)
        if share_bandwidth is not None: action.set_share_bandwidth(share_bandwidth)
        response = self.request.client.get(action)

        return self.get(response[0]['EIPId'])
