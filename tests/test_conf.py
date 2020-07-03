import os
import unittest

from komapy.conf import settings
from komapy.settings import app_settings

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'fixtures'
)


class ConfTest(unittest.TestCase):
    def test_conf_set_and_get_attribute(self):
        app_settings.TEST = 'test'
        self.assertEqual(settings.TEST, 'test')

        settings.BMA_API_HOST = 'localhost:8000'
        self.assertEqual(app_settings.BMA_API_HOST, 'localhost:8000')

    def test_conf_get_default_attribute(self):
        self.assertEqual(settings.TIME_ZONE, 'Asia/Jakarta')

    def test_conf_set_custom_attribute(self):
        settings.CUSTOM = 'custom'
        self.assertEqual(settings.CUSTOM, 'custom')
        self.assertIsNone(getattr(app_settings, 'CUSTOM', None))

    def test_set_attribute_from_dict(self):
        dict_settings = {
            'SETTING0': 'setting0',
            'SETTING1': 'setting1',
        }
        settings.from_dict(dict_settings)
        self.assertEqual(settings.SETTING0, 'setting0')
        self.assertEqual(settings.SETTING1, 'setting1')

    def test_set_attribute_from_json(self):
        json_settings = '{"SETTING2":"setting2","SETTING3":"setting3"}'
        settings.from_json(json_settings)
        self.assertEqual(settings.SETTING2, 'setting2')
        self.assertEqual(settings.SETTING3, 'setting3')

    def test_set_attribute_from_json_file(self):
        json_path = os.path.join(FIXTURE_DIR, 'settings_example.json')
        settings.from_json_file(json_path)
        self.assertEqual(settings.SETTING100, 'setting100')
        self.assertEqual(settings.SETTING200, 'setting200')


if __name__ == '__main__':
    unittest.main()
