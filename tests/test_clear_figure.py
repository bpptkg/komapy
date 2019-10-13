import os
import tempfile
import unittest
import warnings

from komapy.chart import Chart
from komapy.utils import generate_url_safe_filename


class ClearFigureTest(unittest.TestCase):

    def test_render_chart_without_warnings(self):
        config = {
            'title': 'Clear figure test'
        }

        with warnings.catch_warnings(record=True) as w:
            with tempfile.TemporaryDirectory() as tempdirname:
                filename = generate_url_safe_filename()
                fullpath = os.path.join(tempdirname, filename)
                for _ in range(30):
                    chart = Chart(config)
                    chart.render()
                    chart.save(fullpath)
                    chart.clear()
            self.assertEqual(len(w), 0)


if __name__ == '__main__':
    unittest.main()
