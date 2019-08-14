=============
Data Fetching
=============

Most of plot data can be fetch just by providing BMA API name like ``doas``,
``edm``, ``tiltmeter``, etc. Field lookup filtering on the BMA API can be
provided within field ``query_params``. KomaPy will do data query for you, so
you don't need to do it yourself. You just need to specify which data field you
want to plot. Maybe you want to plot ``timestamp`` vs ``slope_distance``, or
maybe you want to plot ``eventdate`` vs ``duration``. See the following example:

.. code-block:: python

    from komapy import Chart

    series = {
        'name': 'edm',
        'query_params': {
            'start_at': '2019-04-01',
            'end_at': '2019-08-01',
            'benchmark': 'BAB0',
            'reflector': 'RB2',
            'ci': True
        },
        'fields': ['timestamp', 'slope_distance'],
        'xaxis_date': True
    }

    chart = Chart({
        'layout': {
            'data': [
                {
                    'series': [
                        series,
                    ]
                }
            ]
        }
    })

    chart.render()
    chart.save('figure.png')

Sometimes, you want to plot other data beside BMA API name, like JSON URL and
CSV file or URL. KomaPy can provide that too. Here it is the example of using
CSV:

.. code-block:: python

    series = {
        # CSV file or URL.
        'csv': '/path/to/csv',
        'csv_params': {
            # Set Pandas read_csv options here.

        },
        'fields': ['timestamp', 'value'],
        'xaxis_date': True,
    }

Another example of using JSON URL:

.. code-block:: python

    series = {
        # URL that return JSON data.
        'url': 'http://example.com/api/v1/data/',
        'query_params': {
            # Set URL query params here.

        },
        'fields': ['timestamp', 'value'],
        'xaxis_date': True,
    }

If you set multiple data resolver in the series config, KomaPy will resolve the
data in the following order: CSV, JSON URL, and BMA API name.

If you want to plot Python object using KomaPy, you can directly pass it to the
``fields`` list. For example:

.. code-block:: python

    x = [1, 2, 3, 4, 5]
    y = x**2

    series = {
        'fields': [x, y]
    }
