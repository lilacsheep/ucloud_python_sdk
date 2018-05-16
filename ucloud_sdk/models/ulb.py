#!/usr/bin/env python
# -*- coding: utf-8 -*-
from addict import Dict
from ucloud_sdk.exception import ULBNotFound, VServerNotFound
from ucloud_sdk.actions.umon import GetMetricOverview, GetMetric
from ucloud_sdk.actions.ulb import *


class BackendSet:

    def __init__(self, vserver, **kwargs):
        self.vserver = vserver
        self._attrs = Dict(kwargs)

    @property
    def id(self):
        return self._attrs.BackendId

    @property
    def resource(self):
        return Dict(resource=self.vserver.ulb.request.uhost.get(self._attrs.ResourceId), port=self._attrs.Port)

    @property
    def status(self):
        return self._attrs.Status

    @property
    def enabled(self):
        return self._attrs.Enabled == 1

    def release(self):
        action = ReleaseBackend(self.vserver.ulb.id, self.id, zone_id=self.vserver.ulb.request.zone.id,
                                region_id=self.vserver.ulb.request.zone.region)
        return self.vserver.ulb.request.client.get(action)

    def __repr__(self):
        return f'<{self.__class__.__name__}(ID={self.id}, Resource={self.resource}, Port={self.resource.port})>'


class VServerSet:

    def __init__(self, ulb, **kwargs):
        self.ulb = ulb
        self._attrs = Dict(kwargs)

    @property
    def id(self):
        return self._attrs.VServerId

    @property
    def name(self):
        return self._attrs.VServerName

    @property
    def protocol(self):
        return self._attrs.Protocol

    @property
    def port(self):
        return self._attrs.FrontendPort

    @property
    def ssl(self):
        return self._attrs.SSLSet

    @property
    def status(self):
        return self._attrs.Status == 0

    @property
    def backends(self):
        return [BackendSet(self, **i) for i in self._attrs.BackendSet]

    def get_backend(self, backend_id) -> BackendSet:
        for i in self.backends:
            if i.id == backend_id:
                return i

    def add_backend(self, resource, port, _type='UHost'):
        action = AllocateBackend(ulb_id=self.ulb.id, vserver_id=self.id, host_id=resource.id, port=port, _type=_type,
            zone_id=self.ulb.request.zone.id, region_id=self.ulb.request.zone.region
        )
        response = self.ulb.request.client.get(action)
        self.reload()
        return self.get_backend(response)

    def delete(self):
        action = DeleteVServer(ulb_id=self.ulb.id, vserver_id=self.id,
                               zone_id=self.ulb.request.zone.id, region_id=self.ulb.request.zone.region)
        self.ulb.request.client.get(action)

    def reload(self):
        action = DescribeVServer(self.ulb.request.client.project_id, ulb_id=self.ulb.id, vserver_id=self.id,
                                 zone_id=self.ulb.request.zone.id, region_id=self.ulb.request.zone.region)
        response = self.ulb.request.client.get(action)
        self._attrs = Dict(**response[0])

class ULBInstance:
    _type = 'ulb'

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
        return [i['EIP'] for i in self.info.IPSet]

    @property
    def vserver(self):
        action = DescribeVServer(self.request.client.project_id, self.id, region_id=self.request.zone.region,
                               zone_id=self.request.zone.id)
        response = self.request.client.get(action)
        return [VServerSet(self, **i) for i in response]

    def get_vserver(self, vserver_id) -> VServerSet:
        action = DescribeVServer(self.request.client.project_id, self.id, vserver_id=vserver_id,
                                 region_id=self.request.zone.region, zone_id=self.request.zone.id)
        response = [VServerSet(self, **i) for i in self.request.client.get(action)]

        for i in response:
            return i
        else:
            raise VServerNotFound(vserver_id)

    def delete(self):
        action = DeleteULB(self.request.client.project_id, self.id, region_id=self.request.zone.region,
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
        return self.get_vserver(self.request.client.get(action))

    def mon(self):
        action = GetMetric(['TotalNetworkOut'], self.id, self._type, region_id=self.request.zone.region,
                               zone_id=self.request.zone.id)
        return self.request.client.get(action)

    def __repr__(self):
        return f'{self.__class__.__name__}<{self.id}-{self.info.Name}>'


class ULB:
    _type = 'ulb'

    def __init__(self, request):
        self.request = request

    def create(self, name, mode='OuterMode', tag=None, remark=None, eip_id=None, share_bandwidth=None, eip_type=None):
        # 创建ULB
        action = CreateULB(project_id=self.request.client.project_id,
                           name=name, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        if tag is not None:
            action.set_tag(tag)
        if remark is not None:
            action.set_remark(remark)
        action.set_mode(mode)

        ulb = self.get(self.request.client.get(action))

        # 创建EIP 并且绑定
        if isinstance(eip_id, str):
            eip = self.request.eip.get(eip_id)
            if eip is not None:
                eip.bind(ulb)

        elif eip_id is None and isinstance(share_bandwidth, str):
            eip = self.request.eip.create_eip(operator_name=eip_type, name=name, tag=tag, remark=remark,
                                              share_bandwidth=share_bandwidth)
            eip.bind(ulb)

        elif eip_id is None and share_bandwidth is None:
            eip = self.request.eip.create_eip(operator_name=eip_type, name=name, tag=tag, remark=remark)
            eip.bind(ulb)

        return ulb

    def get(self, ulb_id) -> ULBInstance:
        for i in self.instances:
            if i.id == ulb_id:
                return i
        else:
            raise ULBNotFound(ulb_id)

    def get_many(self, ids):
        return {i.id: i for i in self.instances if i.id in ids}

    def mon_overview(self):
        action = GetMetricOverview(self._type, zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return self.request.client.get(action)

    @property
    def instances(self):
        action = DescribeULB(zone_id=self.request.zone.id, region_id=self.request.zone.region)
        return [ULBInstance(self.request, **i) for i in self.request.client.get(action)]

