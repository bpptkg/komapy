import unittest

from komapy import exceptions
from komapy import processing


class RegisterAggregationTest(unittest.TestCase):
    """
    Test register custom aggregation functions.
    """

    def test_register_aggregation(self):

        def example(data, params=None):
            pass

        processing.register_aggregation('example', example)

        self.assertEqual(processing.supported_aggregations['example'], example)

        with self.assertRaises(exceptions.ChartError):
            processing.register_aggregation('example', example)

    def test_register_aggregation_with_decorator(self):
        name = 'tests.aggregation.register'

        @processing.register_aggregation(name)
        def example(data, params=None):
            pass

        self.assertTrue(name in processing.supported_aggregations)

    def test_unregister_aggregation(self):
        name = 'tests.aggregation.unregister'

        @processing.register_aggregation(name)
        def example(data, params=None):
            pass

        processing.unregister_aggregation(name)
        self.assertFalse(name in processing.supported_aggregations)


if __name__ == '__main__':
    unittest.main()
