import tempfile
import unittest

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
        self.assertEqual(len(chart.axes), 0)
        self.assertEqual(len(chart.rendered_axes), 0)


if __name__ == '__main__':
    unittest.main()
