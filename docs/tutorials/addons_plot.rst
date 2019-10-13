============
Add-ons Plot
============

Add-ons plot enable you to add other plot to the current axis in particular
subplot figure. Add-ons plot is a list which contains a dictionary of add-ons
configurations. The only required key is ``name``. Other keys are left as
optional parameters and will be passed to the particular add-ons resolver.

For example:

.. code-block:: python

    from komapy import Chart


    def myaddons(axis, **options):
        if options.get('x'):
            # Do something with axis if x is set.
        else:
            # Do something otherwise.


    x = [1, 2, 3]
    y = [1, 2, 3]

    chart = Chart({
        'layout': {
            'data': [
                {
                    'series': [
                        {
                            'fields': [x, y],
                            'addons': [
                                {
                                    'name': myaddons,
                                    'x': 3
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    })

    chart.render()
    chart.save('figure.png')

Sometimes, you need to access the addons plot name by its string name instead of
native function, you can add your addons plot function to the KomaPy global
addons registers:

.. code-block:: python

    from komapy.series import register_addon


    def myaddons(axis, **options):
        if options.get('x'):
            # Do something with axis if x is set.
        else:
            # Do something otherwise.

    register_addon('myaddons', myaddons)

Now you can use ``myaddons`` in your chart configuration:

.. code-block:: python

    from komapy import Chart


    x = [1, 2, 3]
    y = [1, 2, 3]

    chart = Chart({
        'layout': {
            'data': [
                {
                    'series': [
                        {
                            'fields': [x, y],
                            'addons': [
                                {
                                    'name': 'myaddons',
                                    'x': 3
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    })

    chart.render()
    chart.save('figure.png')
