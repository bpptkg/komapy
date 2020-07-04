Set Custom Settings
===================

KomaPy now provides an interface to conveniently set custom settings. For
example, set BMA API key:

.. code-block:: python

    from komapy.conf import settings

    settings.BMA_API_KEY = 'YOUR_API_KEY'

Or set custom BMA API host:

.. code-block:: python

    from komapy.conf import settings

    settings.BMA_API_HOST = '192.168.0.43:8080'

You can also set settings from dictionary object:

.. code-block:: python

    from komapy.conf import settings

    dict_settings = {
        'BMA_API_KEY': 'YOUR_API_KEY',
        'BMA_API_HOST': '192.168.0.43:8080',
    }

    settings.from_dict(dict_settings)

See :doc:`KomaPy settings documentation <../references/settings>` to see all
available settings.
