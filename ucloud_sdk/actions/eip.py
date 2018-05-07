#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ucloud_sdk.actions.base import RegionAction


__all__ = ['DescribeEIP', 'DescribeShareBandwidth', 'AllocateEIP', 'AssociateEIPWithShareBandwidth', 'DisassociateEIPWithShareBandwidth',
           'ReleaseEIP', 'UpdateEIPAttribute', 'BindEIP', 'UnBindEIP']


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


