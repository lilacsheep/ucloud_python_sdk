#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ucloud_sdk.exception import UHostNotFound, UCloudException, UHostAlreadyIsARK
from ucloud_sdk.actions.uhost import *
from ucloud_sdk.models.ulb import *


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
            raise UCloudException(f'Metric Params must be less than 10, now: {len(_metric)}')

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
    def eip_ids(self):
        return [i['IPId'] for i in self.net_cards if i["Type"] != 'Private']

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
        action = ModifyUHostInstanceTag(tag=value, host_id=self.id,
                                        zone_id=self.request.zone.id, region_id=self.request.zone.region)
        self.request.client.get(action)
        self.reload()

    @property
    def name(self):
        return self.info.Name

    @name.setter
    def name(self, value):
        action = ModifyUHostInstanceName(name=value, host_id=self.id,
            zone_id=self.request.zone.id, region_id=self.request.zone.region)
        self.request.client.get(action)
        self.reload()

    @property
    def remark(self):
        return self.info.Remark

    @remark.setter
    def remark(self, value):
        action = ModifyUHostInstanceRemark(remark=value, host_id=self.id,
            zone_id=self.request.zone.id, region_id=self.request.zone.region)
        self.request.client.get(action)
        self.reload()

    @property
    def auto_renew(self):
        return self.info.AutoRenew == 'Yes'

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
    def is_running(self):
        return self.state == 'Running'

    @property
    def is_stopped(self):
        return self.state == 'Stopped'

    @property
    def storage_type(self):
        return self.info.StorageType

    @property
    def time_machine_feature(self):
        return self.info.TimemachineFeature == 'yes'

    def add_to_vserver(self, ulb_id, vserver_id, port):
        ulb = self.request.ulb.get(ulb_id)
        if isinstance(ulb, ULBInstance):
            vserver = ulb.get_vserver(vserver_id)
            if isinstance(vserver, VServerSet):
                return vserver.add_backend(self.id, port)
        return None

    def reboot(self):
        action = RebootUHostInstance(host_id=self.id,
            zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)

    def start(self):
        action = StartUHostInstance(host_id=self.id,
            zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)

    def stop(self):
        action = StopUHostInstance(host_id=self.id,
            zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)

    def terminate(self):
        self.stop()
        action = TerminateUHostInstance(host_id=self.id, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)

    def make_snapshot(self):
        action = CreateUHostInstanceSnapshot(host_id=self.id,
            zone_id=self.request.zone.id, region_id=self.request.zone.region)
        action.set_host_id(self.id)
        return self.request.client.get(action)

    def reload(self):
        action = DescribeUHostInstance(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        action.set_ids([self.id])
        response = self.request.client.get(action)
        self.info = Dict(response[0])

    def upgrade_to_ark(self):
        if not self.time_machine_feature:
            if not self.is_stopped:
                raise UCloudException(f'UHost: {self.id} must be stopped now: {self.state}')
            action = UpgradeToArkUHostInstance(zone_id=self.request.zone.id, region_id=self.request.zone.region)
            action.set_ids([self.id])
            return self.request.client.get(action)
        else:
            raise UHostAlreadyIsARK(self.id)

    def __repr__(self):
        return f'{self.__class__.__name__}<{self.id}-{self.info.Name}>'


class UHost:

    def __init__(self, request):
        self.request = request

    @property
    def instances(self):
        action = DescribeUHostInstance(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return [UHostInstance(self.request, **i) for i in self.request.client.get(action)]

    def get(self, host_id) -> UHostInstance:
        for i in self.instances:
            if i.id == host_id:
                return i
        else:
            raise UHostNotFound(host_id)

    def get_many(self, ids):
        return {i.id: i for i in self.instances if i.id in ids}

    def create(self, image_id, password, cpu=4, memory=8192, name=None, tag=None, remark=None, charge_type='Month', quantity=0,
               boot_disk_space=20, disk_space=20, uhost_type='N1', eip_operator_name='Bgp', eip_share_bandwidth=None):
        action = CreateUHostInstance(image_id, password,
            zone_id=self.request.zone.id, region_id=self.request.zone.region
        )
        action.set_cpu(cpu)
        action.set_memory(memory)
        if isinstance(name, str):
            action.set_name(name)
        if isinstance(tag, str):
            action.set_tag(tag)
        action.set_charge_type(charge_type)
        action.set_quantity(quantity)
        action.set_boot_disk_space(boot_disk_space)
        action.set_disk_space(disk_space)
        action.set_login_mode()
        action.set_uhost_type(uhost_type)
        uhost_id = self.request.client.get(action)[0]
        uhost = self.get(uhost_id)
        if isinstance(remark, str):
            uhost.remark = remark

        eip = self.request.eip.create_eip(eip_operator_name, bandwidth=2, charge_type=charge_type,
                   name=name, tag=tag, remark=remark, share_bandwidth=eip_share_bandwidth)
        eip.bind(uhost)

    def mon_overview(self):
        action = GetMetricOverview('uhost', zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)