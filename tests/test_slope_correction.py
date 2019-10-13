import unittest
import pandas as pd


class SlopeCorrectionTest(unittest.TestCase):

    def test_slope_correction(self):
        slope_data = pd.DataFrame([
            {
                'timestamp': '2019-01-01',
                'slope_distance': 3
            },
            {
                'timestamp': '2019-01-02',
                'slope_distance': 3
            },
            {
                'timestamp': '2019-01-03',
                'slope_distance': 2
            },
            {
                'timestamp': '2019-01-04',
                'slope_distance': 2
            },
            {
                'timestamp': '2019-01-05',
                'slope_distance': 4
            },
            {
                'timestamp': '2019-01-06',
                'slope_distance': 4
            },
        ])

        slope_data['timestamp'] = pd.to_datetime(slope_data['timestamp'])

        err_data = pd.DataFrame([
            {
                'timestamp': '2019-01-03',
                'deviation': -1
            },
            {
                'timestamp': '2019-01-05',
                'deviation': 2
            }
        ])

        err_data['timestamp'] = pd.to_datetime(err_data['timestamp'])

        corrected_data = slope_data.apply(
            lambda item: item.slope_distance + err_data.where(
                err_data.timestamp > item.timestamp).deviation.sum(), axis=1)

        self.assertListEqual(corrected_data.values.tolist(),
                             [4.0, 4.0, 4.0, 4.0, 4.0, 4.0])


if __name__ == '__main__':
    unittest.main()
