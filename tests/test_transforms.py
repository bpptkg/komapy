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


if __name__ == '__main__':
    unittest.main()
