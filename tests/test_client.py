import unittest

from komapy.client import set_api_protocol
from komapy.settings import app_settings


class BMAClientTest(unittest.TestCase):
    def test_set_http_protocol(self):
        set_api_protocol('https')
        self.assertEqual(app_settings.BMA_API_PROTOCOL, 'https')

        set_api_protocol('HTTPS')
        self.assertEqual(app_settings.BMA_API_PROTOCOL, 'https')

        with self.assertRaises(ValueError):
            set_api_protocol('')

        with self.assertRaises(ValueError):
            set_api_protocol(None)


if __name__ == '__main__':
    unittest.main()
