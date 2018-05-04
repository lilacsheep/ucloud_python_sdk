#!/usr/bin/env python
# -*- coding: utf-8 -*-



class UCloudException(Exception):
    pass


class UHostNotFound(Exception):
    pass


class EIPNotFound(Exception):
    pass


class ULBNotFound(Exception):
    pass


class ProjectNotFound(Exception):
    pass


class ShareBandwidthFound(Exception):
    pass