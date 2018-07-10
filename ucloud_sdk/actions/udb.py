#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ucloud_sdk.actions.base import RegionAction


__all__ = ['DeleteUDBInstance', 'RestartUDBInstance', 'StopUDBInstance', 'StartUDBInstance', 'DescribeUDBInstance',
           'DescribeUDBInstancePrice', 'DescribeUDBBackup', 'DeleteUDBBackup', 'DescribeUDBInstanceBackupURL']


class ChangeTypeBaseAction(RegionAction):

    def __init__(self, change_type='Month', quantity=1, **kwargs):
        super(ChangeTypeBaseAction, self).__init__(**kwargs)
        self.set_change_type(change_type)
        self.set_quantity(quantity)

    def set_change_type(self, change_type):
        assert change_type in ['Year', 'Month', 'Dynamic']
        self.set_params('ChangeType', change_type)

    def set_quantity(self, quantity: int):
        self.set_params('Quantity', quantity)


class BaseDBIdAction(RegionAction):

    def __init__(self, db_id, **kwargs):
        super(BaseDBIdAction, self).__init__(**kwargs)
        self.set_db_id(db_id)

    def set_db_id(self, db_id):
        self.set_params('DBId', db_id)

    def set_project_id(self, project_id):
        self.set_params('ProjectId', project_id)


# TODO: 需要确认参数，和控制台业务有出入
class CreateUDBInstance(ChangeTypeBaseAction):
    name = 'CreateUDBInstance'
    response = 'DBId'

    def __init__(self, name, password, db_type, port, disk_space, memory, username='root', use_ssd=False, ssd_type=None,
                 mode='Normal', **kwargs):
        super(CreateUDBInstance, self).__init__(**kwargs)
        self.set_name(name)
        self.set_password(password)
        self.set_db_type(db_type)
        self.set_port(port)
        self.set_disk_space(disk_space)
        self.set_memory(memory)
        self.set_username(username)
        self.set_mode(mode)
        if use_ssd:
            self.set_use_ssd(use_ssd, ssd_type)

    def set_mode(self, mode):
        assert mode in ['Normal', 'HA']
        self.set_params('InstanceMode', mode)

    def set_use_ssd(self, use_ssd, ssd_type):
        assert ssd_type in ['SATA', 'PCI-E']
        self.set_params('UseSSD', use_ssd)

    def set_username(self, username):
        self.set_params('AdminUser', username)

    def set_memory(self, memory):
        self.set_params('MemoryLimit', memory)

    def set_disk_space(self, disk_space):
        assert 20<= disk_space <= 500
        self.set_params('DiskSpace', disk_space)

    def set_port(self, port):
        self.set_params('Port', port)

    def set_db_type(self, db_type):
        assert db_type in ['mysql-5.5', 'mysql-5.1', 'percona-5.5', 'mongodb-2.4', 'mongodb-2.6', 'mysql-5.6', 'percona-5.6']
        self.set_params('DBTypeId', db_type)

    def set_name(self, name):
        assert 6 <=len(name) <=32
        self.set_params('Name', name)

    def set_password(self, password):
        self.set_params('AdminPassword', password)


class DeleteUDBInstance(BaseDBIdAction):
    name = 'DeleteUDBInstance'
    response = 'RetCode'

    def __init__(self, udbc_id=None, *args, **kwargs):
        super(DeleteUDBInstance, self).__init__(*args, **kwargs)
        if isinstance(udbc_id, str):
            self.set_udbc_id(udbc_id)

    def set_udbc_id(self, udbc_id):
        self.set_params('UDBCId', udbc_id)


class StopUDBInstance(BaseDBIdAction):
    name = 'StopUDBInstance'
    response = 'RetCode'

    def __init__(self, force_to_kill=False, *args, **kwargs):
        super(StopUDBInstance, self).__init__(*args, **kwargs)
        if force_to_kill:
            self.set_force_to_kill()

    def set_force_to_kill(self):
        self.set_params('ForceToKill', True)


class StartUDBInstance(BaseDBIdAction):
    name = 'StartUDBInstance'
    response = 'RetCode'


class RestartUDBInstance(BaseDBIdAction):
    name = 'RestartUDBInstance'
    response = 'RetCode'


class DescribeUDBInstance(RegionAction):
    name = 'DescribeUDBInstance'
    response = 'DataSet'

    def __init__(self, db_id=None, class_type=None, udbc_id=None, is_in_udbc=False, include_slaves=False, *args, **kwargs):
        super(DescribeUDBInstance, self).__init__(*args, **kwargs)
        if isinstance(db_id, str):
            self.set_db_id(db_id)
            if include_slaves:
                self.set_include_slaves()
        if isinstance(class_type, str):
            self.set_class_type(class_type)
        if is_in_udbc:
            self.set_is_in_udbc()
            if isinstance(udbc_id, str):
                self.set_udbc_id(udbc_id)

    def set_include_slaves(self):
        self.set_params('IncludeSlaves', True)

    def set_udbc_id(self, udbc_id):
        self.set_params('UDBCId', udbc_id)

    def set_is_in_udbc(self):
        self.set_params('IsInUDBC', True)

    def set_class_type(self, class_type):
        assert class_type in ['SQL', 'NOSQL']
        self.set_params('ClassType', class_type)

    def set_db_id(self, db_id):
        self.set_params('DBId', db_id)

    def set_project_id(self, project_id):
        self.set_params('ProjectId', project_id)


class DescribeUDBInstancePrice(ChangeTypeBaseAction):
    response = 'DataSet'
    name = 'DescribeUDBInstancePrice'

    def __init__(self, memory, disk_space, count=1, use_ssd=False, ssd_type=None, db_type_id='mysql-5.6', mode='Normal', *args, **kwargs):
        super(DescribeUDBInstancePrice, self).__init__(*args, **kwargs)
        self.set_memory(memory)
        self.set_disk_space(disk_space)
        self.set_count(count)
        if use_ssd:
            self.set_use_ssd(ssd_type)
        self.set_db_type(db_type_id)
        self.set_mode(mode)

    def set_mode(self, mode):
        assert mode in ['Normal', 'HA']
        self.set_params('InstanceMode', mode)

    def set_use_ssd(self, ssd_type):
        assert ssd_type in ['SATA', 'PCI-E']
        self.set_params('UseSSD', True)
        self.set_params('SSDType', ssd_type)

    def set_memory(self, memory):
        self.set_params('MemoryLimit', memory)

    def set_disk_space(self, disk_space):
        assert 20<= disk_space <= 500
        self.set_params('DiskSpace', disk_space)

    def set_count(self, count):
        self.set_params('Count', count)

    def set_db_type(self, db_type):
        _all = ['mysql-5.5', 'mysql-5.1', 'percona-5.5', 'mongodb-2.4', 'mongodb-2.6', 'mysql-5.6', 'mysql-5.7']
        assert db_type in _all
        self.set_params('DBTypeId', db_type)


class BackupUDBInstance(BaseDBIdAction):
    name = 'BackupUDBInstance'
    response = 'RetCode'

    def __init__(self, name, use_blacklist=False, *args, **kwargs):
        super(BackupUDBInstance, self).__init__(*args, **kwargs)
        self.set_backup_name(name)
        if use_blacklist:
            self.use_blacklist()

    def set_backup_name(self, name):
        self.set_params('BackupName', name)

    def use_blacklist(self):
        self.set_params('UseBlacklist', True)

    def set_project_id(self, project_id):
        self.set_params('ProjectId', project_id)


class DescribeUDBBackup(RegionAction):
    name = 'DescribeUDBBackup'
    response = 'DataSet'

    def __init__(self, db_id=None, offset=0, limit=20, begin_time=None, end_time=None, backup_type=None, *args, **kwargs):
        super(DescribeUDBBackup, self).__init__(limit=limit, offset=offset, *args, **kwargs)
        if isinstance(db_id, str):
            self.set_db_id(db_id)
        if isinstance(begin_time, int) or isinstance(end_time, int):
            self.set_time_range(begin_time, end_time)
        if isinstance(backup_type, int):
            self.set_params('BackupType', backup_type)

    def set_backup_type(self, backup_type):
        assert backup_type in [0, 1]
        self.set_params('BackupType', backup_type)

    def set_db_id(self, db_id):
        self.set_params('DBId', db_id)

    def set_time_range(self, begin_time, end_time):
        if begin_time:
            self.set_params('BeginTime', begin_time)
        if end_time:
            self.set_params('EndTime', end_time)

    def set_project_id(self, project_id):
        self.set_params('ProjectId', project_id)


class DeleteUDBBackup(RegionAction):
    name = 'DeleteUDBBackup'
    response = 'RetCode'

    def __init__(self, backup_id, backup_zone=None,  *args, **kwargs):
        super(DeleteUDBBackup, self).__init__(*args, **kwargs)
        self.set_backup_id(backup_id)
        if isinstance(backup_zone, str):
            self.set_backup_zone(backup_zone)

    def set_backup_id(self, backup_id):
        self.set_params('BackupId', backup_id)

    def set_backup_zone(self, backup_zone):
        self.set_params('BackupZone', backup_zone)

    def set_project_id(self, project_id):
        self.set_params('ProjectId', project_id)


class DescribeUDBInstanceBackupURL(BaseDBIdAction):
    name = 'DescribeUDBInstanceBackupURL'
    response = 'BackupPath'

    def __init__(self, backup_id, *args, **kwargs):
        super(DescribeUDBInstanceBackupURL, self).__init__(*args, **kwargs)
        self.set_backup_id(backup_id)

    def set_backup_id(self, backup_id):
        self.set_params('BackupId', backup_id)