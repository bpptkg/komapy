import os
import json
import unittest

import numpy as np
import pandas as pd

from komapy.chart import Chart
from komapy.cache import ResolverCache
from komapy.decorators import counter
from komapy.series import Series

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE_DIR = os.path.join(BASE_DIR, 'fixtures')


@counter
def bma_fetch_resource(series, **kwargs):
    """
    Mock BMA API name resolver.
    """
    path = os.path.join(FIXTURE_DIR, 'tiltmeter_selokopo.json')
    with open(path, 'r') as f:
        data = json.load(f)

    return pd.DataFrame(data)


@counter
def csv_fetch_resource(series, **kwargs):
    """
    Mock CSV resolver.
    """
    path = os.path.join(FIXTURE_DIR, 'tiltmeter_selokopo.csv')
    return pd.read_csv(path, **series.csv_params)


class BMAChart(Chart):

    def _fetch_resource(self, series, **kwargs):
        return bma_fetch_resource(series, **kwargs)


class CSVChart(Chart):

    def _fetch_resource(self, series, **kwargs):
        return csv_fetch_resource(series, **kwargs)


class FetchResourceCacheTest(unittest.TestCase):

    def test_fetch_resource_with_bma_api_name(self):
        config = {
            'use_cache': True,
            'layout': {
                'data': [
                    {
                        'series': {
                            'name': 'tiltmeter',
                            'query_params': {
                                'timestamp__gte': '2019-10-01',
                                'timestamp__lt': '2019-11-01',
                                'station': 'selokopo',
                                'nolimit': True
                            },
                            'plot_params': {
                                'zorder': 2,
                                'label': 'X'
                            },
                            'fields': ['timestamp', 'x'],
                            'xaxis_date': True,
                        }
                    },
                    {
                        'series': {
                            'name': 'tiltmeter',
                            'query_params': {
                                'timestamp__gte': '2019-10-01',
                                'timestamp__lt': '2019-11-01',
                                'station': 'selokopo',
                                'nolimit': True
                            },
                            'plot_params': {
                                'zorder': 2,
                                'label': 'Y'
                            },
                            'fields': ['timestamp', 'y'],
                            'xaxis_date': True,
                        }
                    },
                    {
                        'series': {
                            'name': 'tiltmeter',
                            'query_params': {
                                'timestamp__gte': '2019-10-01',
                                'timestamp__lt': '2019-11-01',
                                'station': 'selokopo',
                                'nolimit': True
                            },
                            'plot_params': {
                                'zorder': 2,
                                'label': 'Temperature'
                            },
                            'fields': ['timestamp', 'temperature'],
                            'xaxis_date': True,
                        }
                    },
                ]
            }
        }

        chart = BMAChart(config)
        chart.render()
        self.assertEqual(bma_fetch_resource.count, 1)

    def test_fetch_resource_with_csv(self):
        config = {
            'use_cache': True,
            'layout': {
                'data': [
                    {
                        'series': {
                            'csv': 'http://api.example.com/data.csv',
                            'csv_params': {
                                'delimiter': ',',
                                'header': 0,
                            },
                            'plot_params': {
                                'marker': 'o',
                                'markersize': 6,
                                'linewidth': 1,
                                'label': 'X'
                            },
                            'fields': ['timestamp', 'x'],
                            'xaxis_date': True
                        }
                    },
                    {
                        'series': {
                            'csv': 'http://api.example.com/data.csv',
                            'csv_params': {
                                'delimiter': ',',
                                'header': 0,
                            },
                            'plot_params': {
                                'marker': 'o',
                                'markersize': 6,
                                'linewidth': 1,
                                'label': 'Y'
                            },
                            'fields': ['timestamp', 'y'],
                            'xaxis_date': True
                        }
                    },
                    {
                        'series': {
                            'csv': 'http://api.example.com/data.csv',
                            'csv_params': {
                                'delimiter': ',',
                                'header': 0,
                            },
                            'plot_params': {
                                'marker': 'o',
                                'markersize': 6,
                                'linewidth': 1,
                                'label': 'Temperature'
                            },
                            'fields': ['timestamp', 'temperature'],
                            'xaxis_date': True
                        }
                    },
                ]
            }
        }

        chart = CSVChart(config)
        chart.render()
        self.assertEqual(csv_fetch_resource.count, 1)


class ResolverCacheTest(unittest.TestCase):

    def test_cache_config_with_bma_name(self):
        config = {
            'name': 'seismicity',
            'eventdate__gte': '2019-10-01 12:00:00',
            'eventdate__lt': '2019-10-30 12:00:00',
            'eventtype': 'MP',
            'nolimit': True,
        }
        another_config = {
            'eventdate__lt': '2019-10-30 12:00:00',
            'name': 'seismicity',
            'nolimit': True,
            'eventdate__gte': '2019-10-01 12:00:00',
            'eventtype': 'MP',
        }
        cache = ResolverCache(config)
        another_cache = ResolverCache(another_config)
        self.assertEqual(hash(cache), hash(another_cache))

    def test_cache_config_with_csv(self):
        config = {
            'csv': 'http://api.example.com/data.csv',
            'delimiter': ';',
            'columns': ['timestamp', 'x', 'y', 'temperature']
        }
        another_config = {
            'columns': ['timestamp', 'x', 'y', 'temperature'],
            'delimiter': ';',
            'csv': 'http://api.example.com/data.csv',
        }
        cache = ResolverCache(config)
        another_cache = ResolverCache(another_config)
        self.assertEqual(hash(cache), hash(another_cache))

    def test_cache_config_with_url(self):
        config = {
            'url': 'http://api.example.com/data/',
            'timestamp__gte': '2019-11-01 12:00:00',
            'timestamp__lt': '2019-11-05 12:00:00',
            'type': 'json',
        }
        another_config = {
            'timestamp__gte': '2019-11-01 12:00:00',
            'type': 'json',
            'url': 'http://api.example.com/data/',
            'timestamp__lt': '2019-11-05 12:00:00',
        }
        cache = ResolverCache(config)
        another_cache = ResolverCache(another_config)
        self.assertEqual(hash(cache), hash(another_cache))


class ResolverCacheInstanceCreationTest(unittest.TestCase):

    def test_create_instance_from_series(self):
        series = Series(
            type='bar',
            name='seismicity',
            query_params={
                'eventdate__gte': '2019-10-01',
                'eventdate__lt': '2019-10-30',
                'eventtype': 'MP',
                'nolimit': True,
            },
            fields=['timestamp', 'count'],
            xaxis_date=True,
        )
        instance = ResolverCache.create_instance_from_series(series)
        self.assertTrue(isinstance(instance, ResolverCache))

    def test_create_key_from_series(self):
        series = Series(
            type='bar',
            name='seismicity',
            query_params={
                'eventdate__gte': '2019-10-01',
                'eventdate__lt': '2019-10-30',
                'eventtype': 'ROCKFALL',
                'nolimit': True,
            },
            fields=['timestamp', 'count'],
            xaxis_date=True,
        )
        key = ResolverCache.create_key_from_series(series)
        instance = ResolverCache(
            ResolverCache.get_resolver_cache_config(series))
        self.assertEqual(key, hash(instance))


if __name__ == '__main__':
    unittest.main()
