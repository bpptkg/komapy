import unittest

from komapy import exceptions
from komapy import extensions


class RegisterExtensionsTest(unittest.TestCase):

    def test_register_extensions(self):

        def example(axis, starttime, endtime, **options):
            pass

        extensions.register_extension('example', example)

        self.assertEqual(
            extensions.extension_registers['example']['resolver'], example)

        with self.assertRaises(exceptions.ChartError):
            extensions.register_extension(
                'example', example
            )


if __name__ == '__main__':
    unittest.main()
