import os
import tempfile
import unittest

import pandas as pd

from komapy.chart import Chart
from komapy.exceptions import ChartError


class ChartTest(unittest.TestCase):

    def test_chart_with_none_config(self):
        with self.assertRaises(AttributeError):
            Chart(None)

    def test_chart_with_empty_config(self):
        chart = Chart({})
        chart.render()
        self.assertDictEqual(chart.config, {})
        self.assertEqual(chart.num_subplots, 0)
        self.assertEqual(len(chart.axes), 1)
        self.assertEqual(len(chart.rendered_axes), 0)

    def test_chart_title(self):
        chart = Chart({
            'title': 'Title'
        })
        chart.render()
        self.assertEqual(chart.title, 'Title')

    def test_chart_theme(self):
        chart = Chart({
            'theme': 'seaborn'
        })
        chart.render()
        self.assertEqual(chart.theme, 'seaborn')

    def test_chart_timezone(self):
        chart = Chart({
            'timezone': 'Asia/Jakarta'
        })
        chart.render()
        self.assertEqual(chart.timezone, 'Asia/Jakarta')

    def test_chart_figure_options(self):
        chart = Chart({
            'figure_options': {
                'num': 2,
                'figsize': [6, 8],
                'dpi': 96
            }
        })
        chart.render()
        self.assertDictEqual(chart.figure_options, {
            'num': 2,
            'figsize': [6, 8],
            'dpi': 96
        })

    def test_chart_save_options(self):
        chart = Chart({
            'save_options': {
                'dpi': 300,
                'orientation': 'landscape'
            }
        })
        chart.render()
        self.assertDictEqual(chart.save_options, {
            'dpi': 300,
            'orientation': 'landscape'
        })

    def test_chart_tight_layout(self):
        chart = Chart({
            'tight_layout': {
                'pad': 3,
                'w_pad': 1,
                'h_pad': 1
            }
        })
        chart.render()
        self.assertEqual(chart.tight_layout, {
            'pad': 3,
            'w_pad': 1,
            'h_pad': 1
        })

    def test_chart_create_instance(self):
        data = [
            {'timestamp': '2020-01-01 12:13:45+07:00', 'slope_distance': 1234.500},
            {'timestamp': '2020-01-02 14:08:23+07:00', 'slope_distance': 1234.550},
        ]

        df = pd.DataFrame(data)
        # Ignore time zone info.
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)
        config = {
            'title': 'test_chart_create_instance',
            'layout': {
                'data': [
                    {
                        'series': {
                            'fields': [
                                df['timestamp'],
                                df['slope_distance'],
                            ]
                        }
                    },
                ]
            },
        }
        chart = Chart(config)
        chart.render()
        output = os.path.join(tempfile.gettempdir(), 'output.png')
        chart.save(output)


if __name__ == '__main__':
    unittest.main()
