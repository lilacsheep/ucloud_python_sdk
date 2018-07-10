#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ucloud_sdk.actions.udb import *
from addict import Dict


class UDBSlaveInstanceSet:

    def __init__(self, request, **kwargs):
        self.request = request
        self.attrs = Dict(kwargs)

    @property
    def id(self):
        return self.attrs.DBId

    @property
    def name(self):
        return self.attrs.Name

    @property
    def type(self):
        return self.attrs.DBTypeId

    @property
    def params_group_id(self):
        return self.attrs.ParamGroupId

    @property
    def admin(self):
        return self.attrs.AdminUser

    @property
    def ip(self):
        return self.attrs.VirtualIP

    @property
    def mac(self):
        return self.attrs.VirtualIPMac

    @property
    def port(self):
        return self.attrs.Port

    @property
    def master_db_id(self):
        return self.attrs.SrcDBId

    @property
    def backup_count(self):
        return self.attrs.BackupCount

    @property
    def backup_begin_time(self):
        return self.attrs.BackupBeginTime

    @property
    def backup_duration(self):
        return self.attrs.BackupDuration

    @property
    def backup_blacklist(self):
        return self.attrs.BackupBlacklist

    @property
    def state(self):
        return self.attrs.State

    @property
    def create_time(self):
        return self.attrs.CreateTime

    @property
    def modify_time(self):
        return self.attrs.ModifyTime

    @property
    def expired_time(self):
        return self.attrs.ExpiredTime

    @property
    def change_type(self):
        return self.attrs.ChargeType

    @property
    def memory(self):
        return self.attrs.MemoryLimit

    @property
    def disk_space(self):
        return self.attrs.DiskSpace

    @property
    def use_ssd(self):
        return self.attrs.UseSSD

    @property
    def ssd_type(self):
        return self.attrs.SSDType

    @property
    def role(self):
        return self.attrs.Role

    @property
    def disk_used_size(self):
        return self.attrs.DiskUsedSize

    @property
    def data_file_size(self):
        return self.attrs.DataFileSize

    @property
    def system_file_size(self):
        return self.attrs.SystemFileSize

    @property
    def log_file_size(self):
        return self.attrs.LogFileSize

    @property
    def backup_date(self):
        return self.attrs.BackupDate

    @property
    def instance_mode(self):
        return self.attrs.InstanceMode

    @property
    def price(self):
        action = DescribeUDBInstancePrice(memory=self.memory, disk_space=self.disk_space, db_type_id=self.attrs.DBTypeId,
                                          mode=self.instance_mode, use_ssd=self.use_ssd, ssd_type=self.ssd_type,
                                          zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)[0]['Price']

    def stop(self, force=False):
        action = StopUDBInstance(db_id=self.id, force_to_kill=force, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        self.request.client.get(action)

    def start(self):
        action = StartUDBInstance(db_id=self.id, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        self.request.client.get(action)

    def restart(self):
        action = RestartUDBInstance(db_id=self.id, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        self.request.client.get(action)

    def delete(self):
        action = DeleteUDBInstance(db_id=self.id, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        self.request.client.get(action)



class UDBBackupSet:
    # TODO 其他字段待补充
    def __init__(self, request, **kwargs):
        self.request = request
        self.attrs = Dict(kwargs)

    @property
    def id(self):
        return self.attrs.BackupId

    @property
    def name(self):
        return self.attrs.BackupName

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
    def backup_zone(self):
        return self.attrs.BackupZone

    @property
    def db_id(self):
        return self.attrs.DBId

    @property
    def db_name(self):
        return self.attrs.DBName

    @property
    def backup_url(self):
        action = DescribeUDBInstanceBackupURL(db_id=self.db_id, backup_id=self.id,
                                              zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)

    def delete(self):
        action = DeleteUDBBackup(backup_id=self.id, backup_zone=self.backup_zone,
                                 zone_id=self.request.zone.id, region_id=self.request.zone.region)
        self.request.client.get(action)


class UDBInstanceSet(UDBSlaveInstanceSet):

    @property
    def slave_instance(self):
        return [UDBSlaveInstanceSet(self.request, **i) for i in self.attrs.DataSet]

    @property
    def backup_zone(self):
        return self.attrs.BackupZone

    def backup_list(self, begin_time=None, end_time=None, backup_type=None):
        action = DescribeUDBBackup(db_id=self.id, begin_time=begin_time, end_time=end_time, backup_type=backup_type,
                                   zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return [UDBBackupSet(self.request, **i) for i in self.request.client.get(action)]

    @property
    def zone(self):
        return self.attrs.Zone


class UDB:

    def __init__(self, request):
        self.request = request

    def no_sql_instances(self):
        action = DescribeUDBInstance(offset=0, limit=20, class_type='NOSQL', zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return [UDBInstanceSet(self.request, **i) for i in self.request.client.get(action)]

    def sql_instances(self):
        action = DescribeUDBInstance(offset=0, limit=20, class_type='SQL', zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return [UDBInstanceSet(self.request, **i) for i in self.request.client.get(action)]

    def get_instance(self, db_id, with_slaves=False):
        action = DescribeUDBInstance(db_id=db_id, include_slaves=with_slaves, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return [UDBInstanceSet(self.request, **i) for i in self.request.client.get(action)]

    #TODO create udb

    @property
    def instances(self):
        action = DescribeUDBInstance(offset=0, limit=20, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return [UDBInstanceSet(self.request, **i) for i in self.request.client.get(action)]
