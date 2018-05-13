#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ucloud_sdk.actions.base import RegionAction

__all__ = ['DescribeUHostInstance', 'StopUHostInstance', 'CreateUHostInstance', 'StartUHostInstance', 'RebootUHostInstance',
           'ModifyUHostInstanceRemark', 'CreateUHostInstanceSnapshot', 'ModifyUHostInstanceName', 'ModifyUHostInstanceTag',
           'DescribeUHostTags', 'TerminateUHostInstance', 'UpgradeToArkUHostInstance'
           ]


UHostType = ['Normal', 'SSD', 'BigData', 'GPU', 'GPU_G2',]
ChargeType = ['Year', 'Month', 'Dynamic']
StorageType = ['LocalDisk', 'UDisk']
DiskSpace = [i*10 for i in range(101)]
CPU = [2**i for i in range(5)]
Memory = [2**i for i in range(11, 17)]


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

    def __init__(self, host_id, **kwargs):
        super(StopUHostInstance, self).__init__(**kwargs)
        self.set_host_id(host_id)

    def set_host_id(self, host_id):
        self.set_params('UHostId', host_id)


class CreateUHostInstance(RegionAction):
    name = 'CreateUHostInstance'
    uri = '/'
    response = 'RetCode'

    def __init__(self, image_id, password, **kwargs):
        super(CreateUHostInstance, self).__init__(**kwargs)
        self.set_base_image(image_id)
        self.set_password(password)

    def set_tag(self, tag):
        self.set_params('Tag', tag)

    def set_name(self, name):
        self.set_params('Name', name)

    def set_charge_type(self, charge_type='Month'):
        assert charge_type in ChargeType
        self.set_params('ChargeType', charge_type)

    def set_quantity(self, quantity=1):
        self.set_params('Quantity', quantity)

    def set_charge_month_end(self):
        self.set_params('Quantity', 0)

    def set_uhost_type(self, uhost_type):
        self.set_params('UHostType', uhost_type)

    def set_cpu(self, num=4):
        assert num in CPU
        self.set_params('CPU', num)

    def set_memory(self, num=8192):
        assert num in Memory
        self.set_params('Memory', num)

    def set_gpu(self, num=1):
        assert num in [1, 2, 3, 4]
        self.set_params('GPU', num)

    def set_base_image(self, image_id):
        self.set_params('ImageId', image_id)

    def set_login_mode(self, mode='Password'):
        self.set_params('LoginMode', mode)

    def set_password(self, password):
        self.set_params('Password', password)

    def set_boot_disk_space(self, num=10):
        self.set_params('BootDiskSpace', num)

    def set_disk_space(self, num=20):
        assert num in DiskSpace
        self.set_params('DiskSpace', num)


class StartUHostInstance(StopUHostInstance):
    name = 'StartUHostInstance'


class RebootUHostInstance(StopUHostInstance):
    name = 'RebootUHostInstance'


class ModifyUHostInstanceRemark(StopUHostInstance):
    name = 'ModifyUHostInstanceRemark'

    def __init__(self, remark, *args, **kwargs):
        super(ModifyUHostInstanceRemark, self).__init__(*args, **kwargs)
        self.set_remark(remark)

    def set_remark(self, value):
        self.set_params('Remark', value)


class CreateUHostInstanceSnapshot(StopUHostInstance):
    name = 'CreateUHostInstanceSnapshot'
    response = 'SnapshotName'


class ModifyUHostInstanceName(StopUHostInstance):
    name = 'ModifyUHostInstanceName'

    def __init__(self, name, *args, **kwargs):
        super(ModifyUHostInstanceName, self).__init__(*args, **kwargs)
        self.set_name(name)

    def set_name(self, name):
        self.set_params('Name', name)


class ModifyUHostInstanceTag(StopUHostInstance):
    name = 'ModifyUHostInstanceTag'

    def __init__(self, tag, *args, **kwargs):
        super(ModifyUHostInstanceTag, self).__init__(*args, **kwargs)
        self.set_tag(tag)

    def set_tag(self, tag):
        self.set_params('Tag', tag)


class DescribeUHostTags(RegionAction):
    name = 'DescribeUHostTags'
    response = 'TagSet'


class TerminateUHostInstance(StopUHostInstance):
    name = 'TerminateUHostInstance'
    response = 'UHostIds'
    uri = '/'

    def set_destroy(self, status=1):
        self.set_params('Destroy', status)


class UpgradeToArkUHostInstance(DescribeUHostInstance):
    name = 'UpgradeToArkUHostInstance'
    response = 'RetCode'
    uri = '/'
