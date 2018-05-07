#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ucloud_sdk.actions.base import RegionAction
from addict import Dict
from ucloud_sdk.exception import EIPNotFound, ShareBandwidthFound


class DescribeEIP(RegionAction):
    name = 'DescribeEIP'
    uri = '/'
    response = 'EIPSet'

    def set_eip_id(self, ids):
        for index, _id in enumerate(ids):
            self.set_params(f'EIPIds.{index}', _id)


class DescribeShareBandwidth(RegionAction):
    name = 'DescribeShareBandwidth'
    uri = '/'
    response = 'DataSet'

    def set_bandwidth_ids(self, ids):
        for index, _id in enumerate(ids):
            self.set_params(f'ShareBandwidthIds.{index}', _id)


class AllocateEIP(RegionAction):
    name = 'AllocateEIP'
    uri = '/'
    response = 'EIPSet'

    def __init__(self, operator_name, bandwidth=2, charge_type='Month', **kwargs):
        super(AllocateEIP, self).__init__(**kwargs)
        self.set_charge_type(charge_type)
        self.set_bandwidth(bandwidth)
        self.set_operator(operator_name)

    def set_operator(self, name):
        _mapping = {
            'cn-zj': ['Telecom', 'Unicom', 'Duplet'],
            'cn-sh1': ['Bgp'],
            'cn-sh2': ['Bgp'],
            'cn-gd': ['Bgp'],
            'cn-bj1': ['Bgp'],
            'cn-bj2': ['Bgp'],
        }
        assert name in _mapping.get(self._params['Region'], ['International'])
        self.set_params('OperatorName', name)

    def set_bandwidth(self, bandwidth=2):
        self.set_params('Bandwidth', bandwidth)

    def set_charge_type(self, charge_type):
        _type = ['Year', 'Month', 'Dynamic']
        assert charge_type in _type
        self.set_params('ChargeType', charge_type)

    def set_quantity(self, quantity=1):
        self.set_params('Quantity', quantity)

    def set_tag(self, tag):
        self.set_params('Tag', tag)

    def set_name(self, name):
        self.set_params('Name', name)

    def set_remark(self, remark):
        self.set_params('Remark', remark)

    def set_share_bandwidth(self, share_bandwidth_id):
        self.set_params('PayMode', 'ShareBandwidth')
        self.set_bandwidth(0)
        self.set_params('ShareBandwidthId', share_bandwidth_id)


class AssociateEIPWithShareBandwidth(RegionAction):
    name = 'AssociateEIPWithShareBandwidth'
    uri = '/'
    response = 'RetCode'

    def __init__(self, share_bandwidth, **kwargs):
        super(AssociateEIPWithShareBandwidth, self).__init__(**kwargs)
        self.set_params('ShareBandwidthId', share_bandwidth)

    def set_eip_ids(self, ids):
        for index, _id in enumerate(ids):
            self.set_params(f'EIPIds.{index}', _id)


class DisassociateEIPWithShareBandwidth(AssociateEIPWithShareBandwidth):
    name = 'DisassociateEIPWithShareBandwidth'

    def __init__(self, band_width, **kwargs):
        super(DisassociateEIPWithShareBandwidth, self).__init__(**kwargs)
        self.set_params('Bandwidth', band_width)


class ReleaseEIP(RegionAction):
    name = 'ReleaseEIP'
    uri = '/'
    response = 'RetCode'

    def __init__(self, eip_id, **kwargs):
        super(ReleaseEIP, self).__init__(**kwargs)
        self.set_params('EIPId', eip_id)


class UpdateEIPAttribute(RegionAction):
    name = 'UpdateEIPAttribute'
    uri = '/'
    response = 'RetCode'

    def __init__(self, eip_id, **kwargs):
        super(UpdateEIPAttribute, self).__init__(**kwargs)
        self.set_params('EIPId', eip_id)

    def set_name(self, name):
        self.set_params('Name', name)

    def set_tag(self, tag):
        self.set_params('Tag', tag)

    def set_remark(self, remark):
        self.set_params('Remark', remark)


class BindEIP(RegionAction):
    name = 'BindEIP'
    uri = '/'
    response = 'RetCode'

    def __init__(self, eip_id, resource_type, resource_id, **kwargs):
        super(BindEIP, self).__init__(**kwargs)
        self.set_params('EIPId', eip_id)
        self.set_params('ResourceType', resource_type)
        self.set_params('ResourceId', resource_id)


class UnBindEIP(BindEIP):
    name = 'UnBindEIP'


class EIPAddress:

    def __init__(self, **kwargs):
        self._attrs = Dict(kwargs)

    @property
    def operator(self):
        return self._attrs.OperatorName

    @property
    def ip(self):
        return self._attrs.IP


class UnetEIPResourceSet:

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


class UnetEIPSet:

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
        return UnetEIPResourceSet(**self._attrs.Resource)

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
        return [UnetEIPSet(self.request, **i) for i in self._attrs.EIPSet]


class EIP:

    def __init__(self, request):
        self.request = request

    @property
    def instances(self):
        action = DescribeEIP(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return [UnetEIPSet(self.request, **i) for i in self.request.client.get(action)]

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
            raise ShareBandwidthFound(_id)

    def get(self, eip_id) -> UnetEIPSet:
        for i in self.instances:
            if i.id == eip_id:
                return i
        else:
            raise EIPNotFound(eip_id)

    def create_eip(self, operator_name, bandwidth=2, charge_type='Month', name=None, tag=None, remark=None, share_bandwidth=None):
        action = AllocateEIP(operator_name=operator_name, bandwidth=bandwidth, charge_type=charge_type,
                             zone_id=self.request.zone.id, region_id=self.request.zone.region)
        if name is not None: action.set_name(name)
        if tag is not None: action.set_tag(tag)
        if remark is not None: action.set_remark(remark)
        if share_bandwidth is not None: action.set_share_bandwidth(share_bandwidth)
        response = self.request.client.get(action)

        return self.get(response[0]['EIPId'])
