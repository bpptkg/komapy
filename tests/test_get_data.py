import unittest

from komapy import Chart
from komapy.exceptions import ChartError


class GetDataTest(unittest.TestCase):
    def setUp(self):
        self.config = {
            'title': 'Test Get Series',
            'layout': {
                'data': [
                    {
                        'series': {
                            'index': 'series-0',
                            'fields': [
                                [1, 2, 3],
                                [1, 2, 3],
                            ]
                        }
                    },
                    {
                        'series': {
                            'index': 'series-1',
                            'fields': [
                                [3, 4, 5],
                                [3, 4, 5],
                            ]
                        }
                    },
                ]
            }
        }

    def test_get_series_by_index_name(self):
        chart = Chart(self.config)
        chart.render()

        series = chart.get_series(index='series-0')
        self.assertEqual(series.index, 'series-0')
        self.assertListEqual(series.fields, [[1, 2, 3], [1, 2, 3]])

        series = chart.get_series(index='series-1')
        self.assertEqual(series.index, 'series-1')
        self.assertListEqual(series.fields, [[3, 4, 5], [3, 4, 5]])

    def test_get_series_by_index_number(self):
        chart = Chart(self.config)
        chart.render()

        series = chart.get_series(index=0)
        self.assertEqual(series.index, 'series-0')
        self.assertListEqual(series.fields, [[1, 2, 3], [1, 2, 3]])

        series = chart.get_series(index=1)
        self.assertEqual(series.index, 'series-1')
        self.assertListEqual(series.fields, [[3, 4, 5], [3, 4, 5]])

    def test_get_series_and_data_by_index_name(self):
        chart = Chart(self.config)
        chart.render()

        series_and_data = chart.get_series_and_data(index='series-0')
        self.assertEqual(series_and_data[0].index, 'series-0')
        self.assertListEqual(series_and_data[1], [[1, 2, 3], [1, 2, 3]])

        series_and_data = chart.get_series_and_data(index='series-1')
        self.assertEqual(series_and_data[0].index, 'series-1')
        self.assertListEqual(series_and_data[1], [[3, 4, 5], [3, 4, 5]])

    def test_get_series_and_data_by_index_number(self):
        chart = Chart(self.config)
        chart.render()

        series_and_data = chart.get_series_and_data(index=0)
        self.assertEqual(series_and_data[0].index, 'series-0')
        self.assertListEqual(series_and_data[1], [[1, 2, 3], [1, 2, 3]])

        series_and_data = chart.get_series_and_data(index=1)
        self.assertEqual(series_and_data[0].index, 'series-1')
        self.assertListEqual(series_and_data[1], [[3, 4, 5], [3, 4, 5]])

    def test_get_data_by_index_name(self):
        chart = Chart(self.config)
        chart.render()

        data = chart.get_data(index='series-0')
        self.assertListEqual(data, [[1, 2, 3], [1, 2, 3]])

        data = chart.get_data(index='series-1')
        self.assertListEqual(data, [[3, 4, 5], [3, 4, 5]])

    def test_get_data_by_index_number(self):
        chart = Chart(self.config)
        chart.render()

        data = chart.get_data(index=0)
        self.assertListEqual(data, [[1, 2, 3], [1, 2, 3]])

        data = chart.get_data(index=1)
        self.assertListEqual(data, [[3, 4, 5], [3, 4, 5]])

    def test_get_all_data(self):
        chart = Chart(self.config)
        chart.render()

        data = chart.get_data()
        self.assertListEqual(
            data, [[[1, 2, 3], [1, 2, 3]], [[3, 4, 5], [3, 4, 5]]])


if __name__ == '__main__':
    unittest.main()
