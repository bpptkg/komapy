import os
import json
import unittest

import numpy as np
import pandas as pd

from komapy.chart import Chart
from komapy.decorators import counter

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


if __name__ == '__main__':
    unittest.main()
