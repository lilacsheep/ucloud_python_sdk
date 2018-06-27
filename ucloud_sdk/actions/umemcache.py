#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ucloud_sdk.actions.base import RegionAction


__all__ = ['DeleteUMemcacheGroup', 'DescribeUMemcacheGroup', 'DescribeUMemcachePrice', 'DescribeUMemcacheUpgradePrice',
           'RestartUMemcacheGroup', 'CreateUMemcacheGroup']


class DescribeUMemcachePrice(RegionAction):
    name = 'DescribeUMemcachePrice'
    response = 'DataSet'

    def __init__(self, size=1, change_type='Month', quantity=1, *args, **kwargs):
        super(DescribeUMemcachePrice, self).__init__(*args, **kwargs)
        self.set_size(size)
        self.set_change_type(change_type)
        self.set_quantity(quantity)

    def set_size(self, size: int):
        assert size in [1, 2, 4, 8, 16, 32]
        self.set_params('Size', size)

    def set_change_type(self, change_type):
        assert change_type in ['Year', 'Month', 'Dynamic', 'Trial']
        self.set_params('ChargeType', change_type)

    def set_quantity(self, quantity:int):
        self.set_params('Quantity', quantity)


class DescribeUMemcacheGroup(RegionAction):
    name = 'DescribeUMemcacheGroup'
    response = 'DataSet'

    def __init__(self, group_id=None, *args, **kwargs):
        super(DescribeUMemcacheGroup, self).__init__(*args, **kwargs)
        if isinstance(group_id, str):
            self.set_group_id(group_id)

    def set_group_id(self, group_id):
        self.set_params('GroupId', group_id)


class DeleteUMemcacheGroup(RegionAction):
    name = 'DeleteUMemcacheGroup'
    response = 'RetCode'

    def __init__(self, group_id, *args, **kwargs):
        super(DeleteUMemcacheGroup, self).__init__(*args, **kwargs)
        self.set_group_id(group_id)

    def set_group_id(self, group_id):
        self.set_params('GroupId', group_id)


class RestartUMemcacheGroup(DeleteUMemcacheGroup):
    name = 'RestartUMemcacheGroup'
    response = 'RetCode'


class DescribeUMemcacheUpgradePrice(DeleteUMemcacheGroup):
    name = 'DescribeUMemcacheUpgradePrice'
    response = 'Price'

    def __init__(self, size, *args, **kwargs):
        super(DescribeUMemcacheUpgradePrice, self).__init__(*args, **kwargs)
        self.set_size(size)

    def set_size(self, size: int):
        assert size in [1, 2, 4, 8, 16, 32]
        self.set_params('Size', size)


class CreateUMemcacheGroup(RegionAction):
    name = 'CreateUMemcacheGroup'
    response = 'GroupId'

    def __init__(self, name, size=1, version='1.4.31', config_id='9a891891-c245-4b66-bce8-67e59430d67c',
                 change_type='Month', quantity=1, tag=None, *args, **kwargs):
        super(CreateUMemcacheGroup, self).__init__(*args, **kwargs)
        self.set_name(name)
        self.set_size(size)
        self.set_config_id(config_id)
        # self.set_version(version)
        self.set_change_type(change_type)
        self.set_quantity(quantity)
        if isinstance(tag, str):
            self.set_tag(tag)

    def set_name(self, name):
        assert 6 <=len(name) <=60
        self.set_params('Name', name)

    def set_size(self, size: int):
        assert size in [1, 2, 4, 8, 16, 32]
        self.set_params('Size', size)

    def set_config_id(self, config_id):
        self.set_params('ConfigId', config_id)

    def set_version(self, version):
        self.set_params('Version', version)

    def set_change_type(self, change_type):
        assert change_type in ['Year', 'Month', 'Dynamic', 'Trial']
        self.set_params('ChargeType', change_type)

    def set_quantity(self, quantity:int):
        self.set_params('Quantity', quantity)

    def set_tag(self, tag):
        self.set_params('Tag', tag)

    def set_project_id(self, project_id):
        self.set_params('ProjectId', project_id)


