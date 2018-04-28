#!/usr/bin/env python
# -*- coding: utf-8 -*-
from actions.base import RegionAction


class GetMetric(RegionAction):
    name = 'GetMetric'
    response = 'DataSets'
    uri = '/'

    def __init__(self, MetricName, ResourceId, ResourceType, **kwargs):
        super(GetMetric, self).__init__(**kwargs)
        for index, metric in enumerate(MetricName):
            self.set_params(f'MetricName.{index}', metric)
        self.set_params('ResourceId', ResourceId)
        self.set_params('ResourceType', ResourceType)

    def time_range(self, sec=3600):
        self.set_params('TimeRange', sec)

    def start_time(self, date):
        self.set_params('BeginTime', date)

    def end_time(self, date):
        self.set_params('EndTime', date)


class GetMetricOverview(RegionAction):
    name = 'GetMetricOverview'
    response = 'DataSet'
    uri = '/'

    def __init__(self, ResourceType, **kwargs):
        super(GetMetricOverview, self).__init__(**kwargs)
        self.set_params('ResourceType', ResourceType)