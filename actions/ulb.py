#!/usr/bin/env python
# -*- coding: utf-8 -*-
from actions.base import RegionAction
from actions.umon import GetMetricOverview, GetMetric
from addict import Dict


class DescribeULB(RegionAction):
    name = 'DescribeULB'
    uri = '/'
    response = 'DataSet'


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


class BackendSet:

    def __init__(self, vserver, **kwargs):
        self.vserver = vserver
        self.info = Dict(kwargs)

    @property
    def id(self):
        return self.info.BackendId

    @property
    def resource(self):
        return Dict(
            id=self.info.ResourceId, type=self.info.ResourceType, name=self.info.ResourceName,
            address=self.info.PrivateIP, port=self.info.Port)

    @property
    def status(self):
        return self.info.Status

    @property
    def enabled(self):
        return self.info.Enabled == 1

    def release(self):
        action = ReleaseBackend(self.vserver.ulb.id, self.id, zone_id=self.vserver.ulb.request.zone.id,
                                region_id=self.vserver.ulb.request.zone.region)
        return self.vserver.ulb.request.client.get(action)

    @property
    def instance(self):
        return self.vserver.ulb.request.get_instance(self.resource.id)

    def __repr__(self):
        return f'<{self.__class__.__name__}(ID={self.id}, Host={self.resource.address}, Port={self.resource.port})>'


class VServerSet:

    def __init__(self, ulb, **kwargs):
        self.ulb = ulb
        self.info = Dict(kwargs)

    @property
    def id(self):
        return self.info.VServerId

    @property
    def backends(self):
        return [BackendSet(self, **i) for i in self.info.BackendSet]

    def add_backend(self, host_id, port, _type='UHost'):
        action = AllocateBackend(ulb_id=self.ulb.id, vserver_id=self.id, host_id=host_id, port=port, _type=_type,
            zone_id=self.ulb.request.zone.id, region_id=self.ulb.request.zone.region
        )
        self.ulb.request.client.get(action)

    def delete(self):
        action = DeleteVServer(ulb_id=self.ulb.id, vserver_id=self.id)
        self.ulb.request.client.get(action)


class ULBInstance:

    def __init__(self, request, **kwargs):
        self.info = Dict(kwargs)
        self.request = request

    @property
    def id(self):
        return self.info.ULBId

    @property
    def name(self):
        return self.info.Name

    @property
    def remark(self):
        return self.info.Remark

    @property
    def create_time(self):
        return self.info.CreateTime

    @property
    def tag(self):
        return self.info.Tag

    @property
    def ip_set(self):
        if len(self.info.IPSet):
            temp = self.info.IPSet[0]
            return temp['OperatorName'], temp['EIP']
        return None, None

    @property
    def vserver(self):
        return [VServerSet(self, **i) for i in self.info.VServerSet]

    def delete(self):
        action = DeleteULB(self.request.client.project, self.id, region_id=self.request.zone.region,
                               zone_id=self.request.zone.id)
        return self.request.client.get(action)

    def create_vserver(self, name=None, mode=None, _type=None, port=None):
        action = CreateVServer(ulb_id=self.id, region_id=self.request.zone.region,
                               zone_id=self.request.zone.id, )
        if name is not None:
            action.set_vserver_name(name)
        if mode is not None:
            action.set_protocol(mode)
        if _type is not None:
            action.set_listen_type(_type)
        if port is not None:
            action.set_frontend_port(port)
        return self.request.client.get(action)

    def mon(self):
        action = GetMetric(['TotalNetworkOut'], self.id, 'ulb', region_id=self.request.zone.region,
                               zone_id=self.request.zone.id)
        return self.request.client.get(action)

    def __repr__(self):
        return f'{self.__class__.__name__}<{self.id}-{self.info.Name}>'


class ULB:
    _type = 'ulb'

    def __init__(self, request):
        self.request = request

    def create(self, name, mode='OuterMode', tag=None, remark=None):
        action = CreateULB(project_id=self.request.client.project_id,
                           name=name, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        if tag is not None:
            action.set_tag(tag)
        if remark is not None:
            action.set_remark(remark)
        action.set_mode(mode)
        return self.request.client.get(action)

    def get(self, ulb_id):
        for i in self.instances:
            if i.id == ulb_id:
                return i

    def mon_overview(self):
        action = GetMetricOverview('ulb', zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)

    @property
    def instances(self):
        action = DescribeULB(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return [ULBInstance(self.request, **i) for i in self.request.client.get(action)]

