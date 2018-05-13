#!/usr/bin/env python
# -*- coding: utf-8 -*-


class UCloudException(Exception):
    pass


class UHostNotFound(UCloudException):
    pass


class EIPNotFound(UCloudException):
    pass


class ULBNotFound(UCloudException):
    pass


class ProjectNotFound(UCloudException):
    pass


class ShareBandwidthNotFound(UCloudException):
    pass


class VServerNotFound(UCloudException):
    pass


class UHostAlreadyIsARK(UCloudException):
    pass
