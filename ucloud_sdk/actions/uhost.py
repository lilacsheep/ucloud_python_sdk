#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ucloud_sdk.actions.base import RegionAction
from ucloud_sdk.client import UcloudException
from addict import Dict
from ucloud_sdk.actions import GetMetric, GetMetricOverview


class DescribeUHostInstance(RegionAction):
    name = 'DescribeUHostInstance'
    uri = '/'
    response = 'UHostSet'

    def set_ids(self, ids):
        for index, _id in enumerate(ids):
            self.set_params(f'UHostIds.{index}', _id)


class StopUHostInstance(RegionAction):
    name = 'StopUHostInstance'
    uri = '/'
    response = 'UHostId'

    def set_host_id(self, host_id):
        self.set_params('UHostId', host_id)


class StartUHostInstance(StopUHostInstance):
    name = 'StartUHostInstance'


class RebootUHostInstance(StopUHostInstance):
    name = 'RebootUHostInstance'


class ModifyUHostInstanceRemark(StopUHostInstance):
    name = 'ModifyUHostInstanceRemark'

    def set_remark(self, value):
        self.set_params('Remark', value)


class CreateUHostInstanceSnapshot(StopUHostInstance):
    name = 'CreateUHostInstanceSnapshot'
    response = 'SnapshotName'


class ModifyUHostInstanceName(StopUHostInstance):
    name = 'ModifyUHostInstanceName'

    def set_name(self, name):
        self.set_params('Name', name)


class ModifyUHostInstanceTag(StopUHostInstance):
    name = 'ModifyUHostInstanceTag'

    def set_tag(self, name):
        self.set_params('Tag', name)


class DescribeUHostTags(RegionAction):
    name = 'DescribeUHostTags'
    response = 'TagSet'


class UHostInstance:
    _type = 'uhost'
    _mon_metric = ['CPUUtilization', 'IORead', 'IOWrite', 'DiskReadOps', 'DiskWriteOps', 'NICIn',
              'NICOut', 'NetPacketIn', 'NetPacketOut', 'MemUsage', 'RootSpaceUsage', 'DataSpaceUsage', 'ReadonlyDiskCount',
              'RunnableProcessCount', 'BlockProcessCount', 'ProcessCount', 'TcpConnectCount']

    def __init__(self, request, **kwargs):
        self.info = Dict(kwargs)
        self.request = request

    def mon(self, cpu=False, root_disk=False, data_disk=False, io_read=False, io_write=False, disk_ops=False,
            net_in=False, net_out=False, net_pack_in=False, net_pack_out=False, memory=False, alive_process=False,
            block_process=False, tcp_connect_num=False):
        _metric = []
        if cpu: _metric.append('CPUUtilization')
        if root_disk: _metric.append('RootSpaceUsage')
        if data_disk: _metric.append('DataSpaceUsage')
        if io_read: _metric.append('IORead')
        if io_write: _metric.append('IOWrite')
        if disk_ops: _metric.append('DiskWriteOps')
        if net_in: _metric.append('NICIn')
        if net_out: _metric.append('NICOut')
        if net_pack_in: _metric.append('NetPacketIn')
        if net_pack_out: _metric.append('NetPacketOut')
        if memory: _metric.append('MemUsage')
        if alive_process: _metric.append('ProcessCount')
        if block_process: _metric.append('BlockProcessCount')
        if tcp_connect_num: _metric.append('TcpConnectCount')

        if len(_metric) > 10:
            raise UcloudException(f'Metric Params must be less than 10, now: {len(_metric)}')

        action = GetMetric(MetricName=_metric, ResourceType=self._type, ResourceId=self.id,
                           zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)

    @property
    def net_cards(self):
        return self.info.IPSet

    @property
    def private_ip(self):
        return [i['IP'] for i in self.net_cards if i["Type"] == 'Private']

    @property
    def public_ips(self):
        return [i['IP'] for i in self.net_cards if i["Type"] != 'Private']

    @property
    def eip(self):
        return [self.request.eip.get(i['IPId']) for i in self.net_cards if i["Type"] != 'Private']

    @property
    def id(self):
        return self.info.UHostId

    @property
    def tag(self):
        return self.info.Tag

    @property
    def network_state(self):
        return self.info.NetworkState

    @property
    def cpu(self):
        return self.info.CPU

    @property
    def gpu(self):
        return self.info.GPU

    @property
    def memory(self):
        return self.info.Memory

    @tag.setter
    def tag(self, value):
        tags = [i['Tag'] for i in self.request.tags]
        if value not in tags:
            raise ValueError
        action = ModifyUHostInstanceTag(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        action.set_host_id(self.id)
        action.set_tag(value)
        self.request.client.get(action)
        self.reload()

    @property
    def name(self):
        return self.info.Name

    @name.setter
    def name(self, value):
        action = ModifyUHostInstanceName(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        action.set_host_id(self.id)
        action.set_name(value)
        self.request.client.get(action)
        self.reload()

    @property
    def remark(self):
        return self.info.Remark

    @remark.setter
    def remark(self, value):
        action = ModifyUHostInstanceRemark(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        action.set_host_id(self.id)
        action.set_remark(value)
        self.request.client.get(action)
        self.reload()

    @property
    def auto_renew(self):
        if self.info.AutoRenew == 'Yes':
            return True
        else:
            return False

    @property
    def create_time(self):
        return self.info.CreateTime

    @property
    def expire_time(self):
        return self.info.ExpireTime

    @property
    def charge_type(self):
        return self.info.ChargeType

    @property
    def state(self):
        return self.info.State

    @property
    def storage_type(self):
        return self.info.StorageType

    def reboot(self):
        action = RebootUHostInstance(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        action.set_host_id(self.id)
        return self.request.client.get(action)

    def start(self):
        action = StartUHostInstance(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        action.set_host_id(self.id)
        return self.request.client.get(action)

    def stop(self):
        action = StopUHostInstance(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        action.set_host_id(self.id)
        return self.request.client.get(action)

    def make_snapshot(self):
        action = CreateUHostInstanceSnapshot(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        action.set_host_id(self.id)
        return self.request.client.get(action)

    def reload(self):
        action = DescribeUHostInstance(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        action.set_ids([self.id])
        response = self.request.client.get(action)
        self.info = Dict(response[0])

    def __repr__(self):
        return f'{self.__class__.__name__}<{self.id}-{self.info.Name}>'


class UHost:

    def __init__(self, request):
        self.request = request

    @property
    def instances(self):
        action = DescribeUHostInstance(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return [UHostInstance(self.request, **i) for i in self.request.client.get(action)]

    def get(self, host_id):
        for i in self.instances:
            if i.id == host_id:
                return i

    def mon_overview(self):
        action = GetMetricOverview('uhost', zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)