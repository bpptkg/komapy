import unittest
from komapy import utils


class TestUtils(unittest.TestCase):

    def test_to_pydatetime_from_dictionary(self):
        data = [
            {
                'starttime': '2019-01-01T00:00:00+07:00',
                'endtime': '2019-01-01T00:00:00+07:00',
                'label': 'I',
                'short_desciption': 'Short description I',
                'description': 'Description I',
            },
            {
                'starttime': '2019-01-01T00:00:00+07:00',
                'endtime': '2019-01-01T00:00:00+07:00',
                'label': 'II',
                'short_desciption': 'Short description II',
                'description': 'Description II'
            },
            {
                'starttime': '2019-01-01T00:00:00+07:00',
                'endtime': '2019-01-01T00:00:00+07:00',
                'label': 'III',
                'short_desciption': 'Short description III',
                'description': 'Description III'
            },
        ]

        converted_data = utils.to_pydatetime_from_dictionary(
            data, {'starttime', 'endtime'})

        for item1, item2 in zip(converted_data, data):
            self.assertEqual(item1['starttime'], utils.to_pydatetime(
                item2['starttime']))
            self.assertEqual(item1['endtime'], utils.to_pydatetime(
                item2['endtime']))


if __name__ == '__main__':
    unittest.main()
