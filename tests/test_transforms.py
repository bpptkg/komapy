import unittest

from komapy import exceptions
from komapy import transforms


class RegisterTransformsTest(unittest.TestCase):

    def test_register_transforms(self):

        def example(data, config):
            print(data, config)

        transforms.register_transform('example', example)

        self.assertEqual(transforms.transform_registers['example'], example)

        with self.assertRaises(exceptions.ChartError):
            transforms.register_transform(
                'example', example
            )

    def test_register_transforms_with_decorator(self):
        name = 'tests.transforms.register'

        @transforms.register_transform(name)
        def mytransform(data, config, **kwargs):
            return data

        self.assertTrue(name in transforms.transform_registers)

    def test_unregister_transforms(self):
        name = 'tests.transforms.unregister'

        @transforms.register_transform(name)
        def mytransform(data, config, **kwargs):
            return data

        transforms.unregister_transform(name)
        self.assertFalse(name in transforms.transform_registers)


if __name__ == '__main__':
    unittest.main()
