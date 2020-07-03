===========
Get Started
===========

After you've installed KomaPy package, you can get started to create a chart
using KomaPy chart engine. Because BMA API is a protected API, you should have
API key in order to make an authenticated request to the BMA API. You can set
API key before making any chart instance:

.. code-block:: python

    from komapy.client import set_api_key

    set_api_key('API_KEY')

You can also use access token (``Bearer`` authorization header) from JWT
or OAuth2 authentication:

.. code-block:: python

    from komapy.client import set_access_token

    set_access_token('ACCESS_TOKEN')

You can set custom BMA API host if the host deployed is different from bmaclient
library default:

.. code-block:: python

    from komapy.client import set_api_host

    set_api_host('192.168.0.43:800')

You can also set custom BMA API protocol:

.. code-block:: python

    from komapy.client import set_api_protocol

    set_api_protocol('https')

Now you are ready to create a KomaPy chart. Here it is a simple example to plot
EDM RB2 data:

.. code-block:: python

    from komapy import Chart

    chart = Chart({
        'title': 'RB2',
        'theme': 'seaborn',
        'layout': {
            'data': [
                {
                    'series': [
                        {
                            'name': 'edm',
                            'query_params': {
                                'benchmark': 'BAB0',
                                'reflector': 'RB2',
                                'start_at': '2019-04-01',
                                'end_at': '2019-08-01',
                                'ci': True
                            },
                            'fields': ['timestamp', 'slope_distance'],
                            'xaxis_date': True
                        }
                    ]
                }
            ]
        }
    })

    chart.render()
    chart.save('RB2.png')

As you can see, we create an instance of ``Chart`` class and define its
properties like ``title``, ``theme``, ``layout``, etc. You may want to pay
attention to the ``layout`` property. A chart layout contains ``data`` property,
which represent Matplotlib subplots figure, and it holds information about
``series`` property for each figure. A ``series`` property represent a
Matplotlib ``axis`` instance in KomaPy realm.

In a chart config, you can define one or more layout data, and one or more
series data. The default chart layout in KomaPy is column-based layout, but you
can use grid layout too.

The property ``'name': 'edm'`` tell KomaPy that it should fetch EDM data from
BMA API, and ``query_params`` holds information about data query filtering: ::

    'query_params': {
        'benchmark': 'BAB0',
        'reflector': 'RB2',
        'start_at': '2019-04-01',
        'end_at': '2019-08-01',
        'ci': True
    }

The property ``fields`` is required and it tells KomaPy that it should plot
field named ``timestamp`` on x axis, and field named ``slope_distance`` on y
axis. The property ``xaxis_date`` tells that on the x axis, it should using
date time type instead of regular type.
