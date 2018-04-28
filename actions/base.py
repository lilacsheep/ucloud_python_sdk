#!/usr/bin/env python
# -*- coding: utf-8 -*-


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

    def set_limit(self, limit):
        self.set_params('Limit', limit)