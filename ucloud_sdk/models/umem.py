#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ucloud_sdk.actions.umem import *
from ucloud_sdk.actions.uredis import *
from ucloud_sdk.actions.umon import *
from ucloud_sdk.actions.umemcache import *
from addict import Dict


class UMemSpaceAddressSet:

    def __init__(self, **kwargs):
        self.attrs = Dict(kwargs)

    @property
    def ip(self):
        return self.attrs.IP

    @property
    def port(self):
        return self.attrs.Port


class UMemSpaceSet:

    def __init__(self, request, **kwargs):
        self.request = request
        self.attrs = Dict(kwargs)

    def reload(self):
        action = DescribeUMemSpace(space_id=self.id, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        response = self.request.client.get(action)
        self.attrs = Dict(response[0])

    @property
    def tag(self):
        return self.attrs.Tag

    @property
    def id(self):
        return self.attrs.SpaceId

    @property
    def name(self):
        return self.attrs.Name

    @name.setter
    def name(self, value):
        action = ModifyUMemSpaceName(space_id=self.id, name=value, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        self.request.client.get(action)
        self.attrs.Name = value

    @property
    def zone(self):
        return self.attrs.Zone

    @property
    def create_time(self):
        return self.attrs.CreateTime

    @property
    def expire_time(self):
        return self.attrs.ExpireTime

    @property
    def type(self):
        return self.attrs.Type

    @property
    def protocol(self):
        return self.attrs.Protocol

    @property
    def size(self):
        return self.attrs.Size * 1024

    @property
    def used_size(self):
        return self.attrs.UsedSize

    @property
    def state(self):
        return self.attrs.State

    @property
    def charge_type(self):
        return self.attrs.ChargeType

    @property
    def address(self):
        return UMemSpaceAddressSet(**self.attrs.Address[0])

    @property
    def price(self):
        action = DescribeUMemPrice(size=self.attrs.Size, protocol=self.protocol,change_type=self.charge_type,
                                   quantity=1, type=self.type, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        response = self.request.client.get(action)
        return response[0]['Price']

    def delete(self):
        action = DeleteUMemSpace(space_id=self.id, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        self.request.client.get(action)


class URedisGroupSet:

    def __init__(self, request, **kwargs):
        self.request = request
        self.attrs = Dict(kwargs)

    @property
    def id(self):
        return self.attrs.GroupId

    @property
    def name(self):
        return self.attrs.Name

    @name.setter
    def name(self, value):
        action = ModifyURedisGroupName(group_id=self.id, name=value, zone_id=self.request.zone.id,
                                     region_id=self.request.zone.region)
        self.request.client.get(action)
        self.attrs.Name = value

    @property
    def price(self):
        action = DescribeURedisPrice(size=self.attrs.Size, change_type=self.charge_type, zone_id=self.request.zone.id,
                                     region_id=self.request.zone.region)
        response = self.request.client.get(action)
        return response[0]['Price']

    @property
    def tag(self):
        return self.attrs.Tag

    @property
    def config_id(self):
        return self.attrs.ConfigId

    @property
    def high_availability(self):
        return self.attrs.HighAvailability == 'enable'

    @property
    def version(self):
        return self.attrs.Version

    @property
    def create_time(self):
        return self.attrs.CreateTime

    @property
    def expire_time(self):
        return self.attrs.ExpireTime

    @property
    def auto_backup(self):
        return self.attrs.AutoBackup == 'enable'

    @property
    def backup_time(self):
        return self.attrs.BackupTime

    @property
    def size(self):
        return self.attrs.Size * 1024

    @size.setter
    def size(self, value):
        action = ResizeURedisGroup(group_id=self.id, size=value, zone_id=self.request.zone.id,
                                     region_id=self.request.zone.region)
        self.request.client.get(action)

    def upgrade_price(self, size: int):
        action = DescribeURedisUpgradePrice(group_id=self.id, size=size, zone_id=self.request.zone.id,
                                     region_id=self.request.zone.region)
        return self.request.client.get(action)

    @property
    def used_size(self):
        return self.attrs.UsedSize

    @property
    def state(self):
        return self.attrs.State

    @property
    def charge_type(self):
        return self.attrs.ChargeType

    @property
    def ip(self):
        return self.attrs.VirtualIP

    @property
    def port(self):
        return self.attrs.Port

    def delete(self):
        action = DeleteURedisGroup(group_id=self.id, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        self.request.client.get(action)

    def reload(self):
        action = DescribeURedisGroup(group_id=self.id, zone_id=self.request.zone.id, region_id=self.request.zone.region )
        response = self.request.client.get(action)
        self.attrs = Dict(response[0])


class URedisBackupSet:
    # TODO: 从Backup创建只读实例，或者正常实例， 下载备份
    def __init__(self, request, **kwargs):
        self.request = request
        self.attrs = Dict(**kwargs)

    @property
    def id(self):
        return self.attrs.BackupId

    @property
    def name(self):
        return self.attrs.BackupName

    @property
    def time(self):
        return self.attrs.BackupTime

    @property
    def size(self):
        return self.attrs.BackupSize

    @property
    def type(self):
        return self.attrs.BackupType

    @property
    def state(self):
        return self.attrs.State

    @property
    def zone(self):
        return self.attrs.Zone

    @property
    def group_id(self):
        return self.attrs.GroupId

    @property
    def group_name(self):
        return self.attrs.GroupName

    @property
    def url(self):
        action = DescribeURedisBackupURL(backup_id=self.id, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)



class UMemcacheGroupSet:

    def __init__(self, request, **kwargs):
        self.request = request
        self.attrs = Dict(kwargs)

    @property
    def id(self):
        return self.attrs.GroupId

    @property
    def name(self):
        return self.attrs.Name

    @property
    def config_id(self):
        return self.attrs.ConfigId

    @property
    def ip(self):
        return self.attrs.VirtualIP

    @property
    def port(self):
        return self.attrs.Port

    @property
    def size(self):
        return self.attrs.Size

    @property
    def used_size(self):
        return self.attrs.UsedSize

    @property
    def version(self):
        return self.attrs.Version

    @property
    def state(self):
        return self.attrs.State

    @property
    def create_time(self):
        return self.attrs.CreateTime

    @property
    def expire_time(self):
        return self.attrs.ExpireTime

    @property
    def modify_time(self):
        return self.attrs.ModifyTime

    @property
    def tag(self):
        return self.attrs.Tag

    @property
    def charge_type(self):
        return self.attrs.ChargeType

    @property
    def price(self):
        action = DescribeUMemcachePrice(size=self.size, change_type=self.charge_type, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)[0]['Price']

    def upgrade_price(self, size):
        action = DescribeUMemcacheUpgradePrice(group_id=self.id, size=size, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)

    def delete(self):
        action = DeleteUMemcacheGroup(group_id=self.id, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        self.request.client.get(action)

    def restart(self):
        action = RestartUMemcacheGroup(group_id=self.id, zone_id=self.request.zone.id,
                                      region_id=self.request.zone.region)
        self.request.client.get(action)



class UMemDistributed:

    def __init__(self, request):
        self.request = request

    def get(self, space_id):
        action = DescribeUMemSpace(space_id=space_id, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        response = self.request.client.get(action)
        return UMemSpaceSet(self.request, **response[0])

    @property
    def instances(self):
        action = DescribeUMemSpace(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return [UMemSpaceSet(self.request, **i) for i in self.request.client.get(action)]

    def get_many(self, ids):
        return [i for i in self.instances if i.id in ids]

    def create_redis(self, name, size: int, protocol='redis', change_type='Month', quantity=0, type='double'):
        action = CreateUMemSpace(name=name, size=size, protocol=protocol, change_type=change_type, quantity=quantity, type=type,
                                 zone_id=self.request.zone.id, region_id=self.request.zone.region)
        response = self.request.client.get(action)
        return self.get(response)

    def create_memcache(self, name, size: int, protocol='memcache', change_type='Month', quantity=0, type='double'):
        action = CreateUMemSpace(name=name, size=size, protocol=protocol, change_type=change_type, quantity=quantity, type=type,
                                 zone_id=self.request.zone.id, region_id=self.request.zone.region)
        response = self.request.client.get(action)
        return self.get(response)

    def mon_overview(self):
        action = GetMetricOverview('umem', zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)



class URedis:

    def __init__(self, request):
        self.request = request

    def get(self, group_id):
        action = DescribeURedisGroup(group_id=group_id, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        response = self.request.client.get(action)
        return URedisGroupSet(self.request, **response[0])

    def get_many(self, ids):
        return [i for i in self.instances if i.id in ids]

    @property
    def instances(self):
        action = DescribeURedisGroup(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return [URedisGroupSet(self.request, **i) for i in self.request.client.get(action)]

    def backups(self):
        action = DescribeURedisBackup(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return [URedisBackupSet(self.request, **i) for i in self.request.client.get(action)]

    def create(self, name, high_availability, size=1, redis_version='3.0', change_type='Month', quantity=1, tag=None, password=None,
                 config_id='03f58ca9-b64d-4bdd-abc7-c6b9a46fd801', auto_backup=False, backup_time=3):
        action = CreateURedisGroup(name, high_availability, size=size, redis_version=redis_version, change_type=change_type,
                                   quantity=quantity, tag=tag, password=password, config_id=config_id,
                                   auto_backup=auto_backup, backup_time=backup_time, zone_id=self.request.zone.id,
                                   region_id=self.request.zone.region)
        response = self.request.client.get(action)
        return self.get(response)

    def mon_overview(self):
        action = GetMetricOverview('uredis', zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)


class UMemcache:

    def __init__(self, request):
        self.request = request

    def get(self, group_id):
        action = DescribeUMemcacheGroup(group_id=group_id, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        response = self.request.client.get(action)
        return UMemcacheGroupSet(self.request, **response[0])

    def get_many(self, ids):
        return [i for i in self.instances if i.id in ids]

    @property
    def instances(self):
        action = DescribeUMemcacheGroup(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return [UMemcacheGroupSet(self.request, **i) for i in self.request.client.get(action)]

    def create(self, name, size=1, version='1.4.31', config_id='9a891891-c245-4b66-bce8-67e59430d67c',
                 change_type='Month', quantity=1, tag=None):
        action = CreateUMemcacheGroup(name, size=size, config_id=config_id,
                 change_type=change_type, quantity=quantity, tag=tag, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        response = self.request.client.get(action)
        return self.get(response)

    def mon_overview(self):
        action = GetMetricOverview('umemcache', zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)

class UMem:

    def __init__(self, request):
        self.request = request
        self.distributed = UMemDistributed(self.request)
        self.uredis = URedis(self.request)
        self.memcache = UMemcache(self.request)