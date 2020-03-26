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

    def test_register_extensions_with_decorators(self):
        name = 'tests.extension.register'

        @extensions.register_extension(name)
        def example(axis, starttime, endtime, **kwargs):
            pass

        self.assertTrue(name in extensions.extension_registers)

    def test_unregister_extensions(self):
        name = 'tests.extensions.unregister'

        @extensions.register_extension(name)
        def example(axis, starttime, endtime, **kwargs):
            pass

        extensions.unregister_extension(name)
        self.assertFalse(name in extensions.extension_registers)


if __name__ == '__main__':
    unittest.main()
