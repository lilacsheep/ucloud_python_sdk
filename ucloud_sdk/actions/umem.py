#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ucloud_sdk.actions.base import RegionAction


__all__ = ['GetUMemSpaceState', 'DescribeUMemPrice', 'ModifyUMemSpaceName', 'DeleteUMemSpace', 'ResizeUMemSpace',
           'DescribeUMemSpace', 'DescribeUMemUpgradePrice', 'CreateUMemSpace']


class DescribeUMemSpace(RegionAction):
    name = 'DescribeUMemSpace'
    response = 'DataSet'

    def __init__(self, space_id=None, *args, **kwargs):
        super(DescribeUMemSpace, self).__init__(*args, **kwargs)
        if isinstance(space_id, str):
            self.set_space_id(space_id)

    def set_space_id(self, space_id):
        self.set_params('SpaceId', space_id)

    def set_project_id(self, project_id):
        self.set_params('ProjectId', project_id)


class CreateUMemSpace(RegionAction):
    name = 'CreateUMemSpace'
    response = 'SpaceId'

    def __init__(self, size: int, name, protocol='redis', change_type='Month', quantity=0, type='double', *args, **kwargs):
        super(CreateUMemSpace, self).__init__(*args, **kwargs)
        self.set_name(name)
        self.set_size(size)
        self.set_type(type)
        self.set_protocol(protocol)
        self.set_change_type(change_type)
        self.set_quantity(quantity)

    def set_type(self, type):
        assert type in ['single', 'double']
        self.set_params('Type', type)

    def set_size(self, size):
        assert size in range(16, 1025)
        self.set_params('Size', size)

    def set_name(self, name):
        assert 6 <= len(name) <=63
        self.set_params('Name', name)

    def set_change_type(self, change_type):
        assert change_type in ['Year', 'Month', 'Dynamic', 'Trial']
        self.set_params('ChargeType', change_type)

    def set_quantity(self, quantity:int):
        self.set_params('Quantity', quantity)

    def set_protocol(self, protocol):
        self.set_params('Protocol', protocol)

    def set_project_id(self, project_id):
        self.set_params('ProjectId', project_id)


class DescribeUMemPrice(RegionAction):
    name = 'DescribeUMemPrice'
    response = 'DataSet'

    def __init__(self, size: int, protocol='redis', change_type='Month', quantity=0, type='double', *args, **kwargs):
        super(DescribeUMemPrice, self).__init__(*args, **kwargs)
        self.set_size(size)
        self.set_type(type)
        self.set_protocol(protocol)
        self.set_change_type(change_type)
        self.set_quantity(quantity)

    def set_type(self, type):
        assert type in ['single', 'double']
        self.set_params('Type', type)

    def set_size(self, size):
        assert size in range(1, 1025)
        self.set_params('Size', size)

    def set_change_type(self, change_type):
        assert change_type in ['Year', 'Month', 'Dynamic', 'Trial']
        self.set_params('ChargeType', change_type)

    def set_quantity(self, quantity:int):
        self.set_params('Quantity', quantity)

    def set_protocol(self, protocol):
        self.set_params('Protocol', protocol)

    def set_project_id(self, project_id):
        self.set_params('ProjectId', project_id)


class ModifyUMemSpaceName(RegionAction):
    name = 'ModifyUMemSpaceName'
    response = 'RetCode'

    def __init__(self, space_id, name,  *args, **kwargs):
        super(ModifyUMemSpaceName, self).__init__(*args, **kwargs)
        self.set_name(name)
        self.set_space_id(space_id)

    def set_space_id(self, space_id):
        self.set_params('SpaceId', space_id)

    def set_name(self, name):
        assert 6 <= len(name) <=63
        self.set_params('Name', name)

    def set_project_id(self, project_id):
        self.set_params('ProjectId', project_id)


class GetUMemSpaceState(RegionAction):
    name = 'GetUMemSpaceState'
    response = 'State'

    def __init__(self, space_id, *args, **kwargs):
        super(GetUMemSpaceState, self).__init__(*args, **kwargs)
        self.set_space_id(space_id)

    def set_space_id(self, space_id):
        self.set_params('SpaceId', space_id)


class DeleteUMemSpace(GetUMemSpaceState):
    name = 'DeleteUMemSpace'
    response = 'RetCode'


class ResizeUMemSpace(RegionAction):
    name = 'ResizeUMemSpace'
    response = 'RetCode'

    def __init__(self, size: int, space_id, *args, **kwargs):
        super(ResizeUMemSpace, self).__init__(*args, **kwargs)
        self.set_space_id(space_id)
        self.set_size(size)

    def set_size(self, size):
        assert size in range(1, 1025)
        self.set_params('Size', size)

    def set_space_id(self, space_id):
        self.set_params('SpaceId', space_id)


class DescribeUMemUpgradePrice(RegionAction):
    name = 'DescribeUMemUpgradePrice'
    response = 'Price'

    def __init__(self, space_id, size: int, type='double', *args, **kwargs):
        super(DescribeUMemUpgradePrice, self).__init__(*args, **kwargs)
        self.set_size(size)
        self.set_type(type)
        self.set_space_id(space_id)

    def set_space_id(self, space_id):
        self.set_params('SpaceId', space_id)

    def set_type(self, type):
        assert type in ['single', 'double']
        self.set_params('Type', type)

    def set_size(self, size):
        assert size in range(1, 1025)
        self.set_params('Size', size)

    def set_project_id(self, project_id):
        self.set_params('ProjectId', project_id)
