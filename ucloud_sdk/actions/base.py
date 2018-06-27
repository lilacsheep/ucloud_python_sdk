#!/usr/bin/env python
# -*- coding: utf-8 -*-
from addict import Dict


class BaseAction:
    name = None
    uri = None
    need_project = True
    method = 'get'
    response = None

    def __init__(self):
        self._params = {'Action': self.name}

    def set_params(self, key, value):
        self._params[key] = value

    @property
    def params(self):
        return self._params


class RegionAction(BaseAction):

    def __init__(self, region_id=None, zone_id=None, limit=None, offset=None):
        super(RegionAction, self).__init__()
        if region_id is not None:
            self.set_params('Region', region_id)
        if zone_id is not None:
            self.set_params('Zone', zone_id)
        if isinstance(limit, int):
            self.set_params('Limit', limit)
        if isinstance(offset, int):
            self.set_params('Offset', offset)

    def set_region(self, region_id):
        self.set_params('Region', region_id)

    def set_zone(self, zone_id):
        self.set_params('Zone', zone_id)

    def set_offset(self, offset):
        self.set_params('Offset', offset)

    def set_limit(self, limit):
        self.set_params('Limit', limit)


class ProjectSet:

    def __init__(self, **kwargs):
        self._attrs = Dict(kwargs)

    @property
    def id(self):
        return self._attrs.ProjectId

    @property
    def name(self):
        return self._attrs.ProjectName

    @property
    def create_time(self):
        return self._attrs.CreateTime

    @property
    def is_default(self):
        return self._attrs.IsDefault.lower() == 'yes'


class GetProjectList(BaseAction):
    response = 'ProjectSet'
    uri = 'usub_account'
    name = 'GetProjectList'