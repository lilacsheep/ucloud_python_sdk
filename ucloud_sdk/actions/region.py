#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ucloud_sdk.actions.base import BaseAction


class GetRegion(BaseAction):
    uri = '/'
    name = 'GetRegion'
    need_project = False
    response = 'Regions'
