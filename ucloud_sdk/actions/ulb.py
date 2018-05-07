#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ucloud_sdk.actions.base import RegionAction
__all__ = ['DescribeULB', 'DescribeVServer', 'AllocateBackend', 'ReleaseBackend', 'DeleteVServer', 'CreateVServer',
           'CreateULB', 'DeleteULB']


class DescribeULB(RegionAction):
    name = 'DescribeULB'
    uri = '/'
    response = 'DataSet'


class DescribeVServer(RegionAction):
    name = 'DescribeVServer'
    uri = '/'
    response = 'DataSet'

    def __init__(self, project_id, ulb_id, vserver_id=None, **kwargs):
        super(DescribeVServer, self).__init__(**kwargs)
        self.set_params('ULBId', ulb_id)
        self.set_params('ProjectId', project_id)
        if isinstance(vserver_id, str):
            self.set_params('VServerId', vserver_id)

class AllocateBackend(RegionAction):
    name = 'AllocateBackend'
    uri = '/'
    response = 'BackendId'

    def __init__(self, ulb_id, vserver_id, host_id, port, _type='UHost', **kwargs):
        super(AllocateBackend, self).__init__(**kwargs)
        self.set_params('ULBId', ulb_id)
        self.set_params('VServerId', vserver_id)
        self.set_params('ResourceType', _type)
        self.set_params('ResourceId', host_id)
        self.set_params('Port', int(port))
        self.set_params('Enabled', 1)


class ReleaseBackend(RegionAction):
    name = 'ReleaseBackend'
    uri = '/'
    response = 'RetCode'

    def __init__(self, ulb_id, backend_id, **kwargs):
        super(ReleaseBackend, self).__init__(**kwargs)
        self.set_params('BackendId', backend_id)
        self.set_params('ULBId', ulb_id)


class DeleteVServer(RegionAction):
    name = 'DeleteVServer'
    uri = '/'
    response = 'RetCode'

    def __init__(self, ulb_id, vserver_id, **kwargs):
        super(DeleteVServer, self).__init__(**kwargs)
        self.set_params('VServerId', vserver_id)
        self.set_params('ULBId', ulb_id)


class CreateVServer(RegionAction):
    name = 'CreateVServer'
    uri = '/'
    response = 'VServerId'
    listen_type = {
        'RequestProxy': ['HTTP', 'HTTPS'],
        'PacketsTransmit': ['TCP', 'UDP']
    }
    port_range = list(range(1, 65536))

    def __init__(self, ulb_id, **kwargs):
        super(CreateVServer, self).__init__(**kwargs)
        self.set_params('ULBId', ulb_id)
        self.set_params('ListenType', 'RequestProxy')
        self.set_params('Protocol', 'HTTP')
        self.set_params('FrontendPort', 80)

    def set_vserver_name(self, name):
        self.set_params('VServerName', name)

    def set_protocol(self, mode: str):
        if mode not in self.listen_type[self.params['ListenType']]:
            raise ValueError
        self.set_params('Protocol', mode)

    def set_listen_type(self, _type):
        if _type not in self.listen_type:
            self.set_params('ListenType', _type)
        else:
            raise ValueError

    def set_frontend_port(self, port):
        if port not in self.port_range:
            raise ValueError
        else:
            self.set_params('FrontendPort', port)


class CreateULB(RegionAction):
    name = 'CreateULB'
    uri = '/'
    response = 'ULBId'

    def __init__(self, project_id, name, **kwargs):
        super(CreateULB, self).__init__(**kwargs)
        self.set_params('ProjectId', project_id)
        self.set_params('ULBName', name)
        self.set_params('ChargeType', 'Month')

    def set_mode(self, mode):
        self.set_params(mode, 'Yes')

    def set_tag(self, tag):
        self.set_params('Tag', tag)

    def set_remark(self, remark):
        self.set_params('Remark', remark)


class DeleteULB(RegionAction):
    name = 'DeleteULB'
    uri = '/'
    response = 'RetCode'

    def __init__(self, project_id, ulb_id, **kwargs):
        super(DeleteULB, self).__init__(**kwargs)
        self.set_params('ProjectId', project_id)
        self.set_params('ULBId', ulb_id)
