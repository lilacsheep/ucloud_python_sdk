#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ucloud_sdk.actions.base import RegionAction

__all__ = ['CreateURedisGroup', 'DescribeURedisGroup', 'DeleteURedisGroup', 'ModifyURedisGroupName', 'DescribeURedisPrice',
           'ResizeURedisGroup', 'DescribeURedisUpgradePrice', 'DescribeURedisBackup', 'DescribeURedisBackupURL']


class CreateURedisGroup(RegionAction):
    name = 'CreateURedisGroup'
    response = 'GroupId'

    def __init__(self, name, high_availability, size=1, redis_version='3.0', change_type='Month', quantity=1, tag=None, password=None,
                 config_id='03f58ca9-b64d-4bdd-abc7-c6b9a46fd801', auto_backup=False, backup_time=3,
                 *args, **kwargs):
        super(CreateURedisGroup, self).__init__(*args, **kwargs)
        self.set_name(name)
        self.set_size(size)
        self.set_backup_time(backup_time)
        self.set_auto_backup(auto_backup)
        self.set_high_availability(high_availability)
        self.set_config_id(config_id)
        self.set_redis_version(redis_version)
        self.set_change_type(change_type)
        self.set_quantity(quantity)
        if isinstance(tag, str):
            self.set_tag(tag)
        if isinstance(password, str):
            self.set_password(password)

    def set_password(self, password):
        self.set_params('Password', password)

    def set_tag(self, tag):
        self.set_params('Tag', tag)

    def set_change_type(self, change_type):
        assert change_type in ['Year', 'Month', 'Dynamic', 'Trial']
        self.set_params('ChargeType', change_type)

    def set_quantity(self, quantity:int):
        self.set_params('Quantity', quantity)

    def set_redis_version(self, version):
        assert version in ['3.0', '3.2', '4.0']
        self.set_params('Version', version)

    def set_config_id(self, config_id):
        self.set_params('ConfigId', config_id)

    def set_high_availability(self, mode):
        assert isinstance(mode, bool)
        mode = 'enable' if mode else 'disable'
        self.set_params('HighAvailability', mode)

    def set_size(self, size):
        assert size in [1, 2, 4, 8, 16, 32]
        self.set_params('Size', size)

    def set_auto_backup(self, mode: bool):
        assert isinstance(mode, bool)
        mode = 'enable' if mode else 'disable'
        self.set_params('AutoBackup', mode)

    def set_backup_time(self, hour):
        assert hour in range(0, 24)
        self.set_params('BackupTime', hour)

    def set_name(self, name):
        assert 6 <= len(name) <=63
        self.set_params('Name', name)

    def set_project_id(self, project_id):
        self.set_params('ProjectId', project_id)


class DescribeURedisGroup(RegionAction):
    name = 'DescribeURedisGroup'
    response = 'DataSet'

    def __init__(self, group_id=None, *args, **kwargs):
        super(DescribeURedisGroup, self).__init__(*args, **kwargs)
        if group_id:
            self.set_group_id(group_id)

    def set_project_id(self, project_id):
        self.set_params('ProjectId', project_id)

    def set_group_id(self, group_id):
        self.set_params('GroupId', group_id)


class DeleteURedisGroup(RegionAction):
    name = 'DeleteURedisGroup'
    response = 'RetCode'

    def __init__(self, group_id, *args, **kwargs):
        super(DeleteURedisGroup, self).__init__(*args, **kwargs)
        self.set_group_id(group_id)

    def set_project_id(self, project_id):
        self.set_params('ProjectId', project_id)

    def set_group_id(self, group_id):
        self.set_params('GroupId', group_id)


class ModifyURedisGroupName(RegionAction):
    name = 'ModifyURedisGroupName'
    response = 'RetCode'

    def __init__(self, group_id, name, *args, **kwargs):
        super(ModifyURedisGroupName, self).__init__(*args, **kwargs)
        self.set_name(name)
        self.set_group_id(group_id)

    def set_group_id(self, group_id):
        self.set_params('GroupId', group_id)

    def set_name(self, name):
        assert 6 <= len(name) <=63
        self.set_params('Name', name)

    def set_project_id(self, project_id):
        self.set_params('ProjectId', project_id)


class DescribeURedisPrice(RegionAction):
    name = 'DescribeURedisPrice'
    response = 'DataSet'

    def __init__(self, size: int, change_type='Month', quantity=1, *args, **kwargs):
        super(DescribeURedisPrice, self).__init__(*args, **kwargs)
        self.set_size(size)
        self.set_change_type(change_type)
        self.set_quantity(quantity)

    def set_size(self, size):
        assert size in [1, 2, 4, 8, 16, 32]
        self.set_params('Size', size)

    def set_change_type(self, change_type):
        assert change_type in ['Year', 'Month', 'Dynamic', 'Trial']
        self.set_params('ChargeType', change_type)

    def set_quantity(self, quantity:int):
        self.set_params('Quantity', quantity)

    def set_project_id(self, project_id):
        self.set_params('ProjectId', project_id)


class ResizeURedisGroup(RegionAction):
    name = 'ResizeURedisGroup'
    response = 'RetCode'

    def __init__(self, group_id, size: int, *args, **kwargs):
        super(ResizeURedisGroup, self).__init__(*args, **kwargs)
        self.set_size(size)
        self.set_group_id(group_id)

    def set_group_id(self, group_id):
        self.set_params('GroupId', group_id)

    def set_size(self, size):
        assert size in [1, 2, 4, 8, 16, 32]
        self.set_params('Size', size)


class DescribeURedisUpgradePrice(ResizeURedisGroup):
    name = 'DescribeURedisUpgradePrice'
    response = 'Price'


class DescribeURedisBackup(DescribeURedisGroup):
    name = 'DescribeURedisBackup'
    response = 'DataSet'


class DescribeURedisBackupURL(RegionAction):
    name = 'DescribeURedisBackupURL'
    response = 'BackupURL'

    def __init__(self, backup_id, region_flag=False, *args, **kwargs):
        super(DescribeURedisBackupURL, self).__init__(*args, **kwargs)
        self.set_backup_id(backup_id)
        self.set_region_flag(region_flag)

    def set_backup_id(self, backup_id):
        self.set_params('BackupId', backup_id)

    def set_region_flag(self, region_flag):
        self.set_params('RegionFlag', region_flag)

    def set_project_id(self, project_id):
        self.set_params('ProjectId', project_id)