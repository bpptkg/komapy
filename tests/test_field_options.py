import unittest

from komapy.chart import Chart


class FieldOptionsTest(unittest.TestCase):

    def test_field_options(self):

        def series(axis, **options):
            axis.plot(options['x'], options['y'])
            return axis

        config = {
            'layout': {
                'data': [
                    {
                        'series': {
                            'fields': series,
                            'field_options': {
                                'x': [1, 2, 3],
                                'y': [1, 2, 3]
                            }
                        }
                    }
                ]
            }
        }

        chart = Chart(config)
        chart.render()

        axis = chart.rendered_axes[0][0]
        x = axis.lines[0].get_xdata()
        y = axis.lines[0].get_ydata()
        self.assertListEqual(list(x), [1, 2, 3])
        self.assertListEqual(list(y), [1, 2, 3])


if __name__ == '__main__':
    unittest.main()
