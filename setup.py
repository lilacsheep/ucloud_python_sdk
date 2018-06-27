#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(name='ucloud_sdk', version='0.1.25', install_requires=['requests', 'addict'],
      py_modules=[
          'ucloud_sdk.actions.base',
          'ucloud_sdk.actions.eip',
          'ucloud_sdk.actions.region',
          'ucloud_sdk.actions.sms',
          'ucloud_sdk.actions.uhost',
          'ucloud_sdk.actions.ulb',
          'ucloud_sdk.actions.umon',
          'ucloud_sdk.actions.udb',
          'ucloud_sdk.actions.uredis',
          'ucloud_sdk.actions.umen',
          'ucloud_sdk.actions.umencache',
          'ucloud_sdk.models.uhost',
          'ucloud_sdk.models.eip',
          'ucloud_sdk.models.ulb',
          'ucloud_sdk.models.udb',
          'ucloud_sdk.models.umem',
          'ucloud_sdk.client',
          'ucloud_sdk.exception',
          'ucloud_sdk.UCloud'],
      )