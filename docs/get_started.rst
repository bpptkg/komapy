===========
Get Started
===========

After you've installed KomaPy package, you can get started to create a chart
using KomaPy chart engine. Because BMA API is protected API, you should have API
key in order to make an authenticated request to the BMA API. You can set API
key before making any chart instance:

.. code-block:: python

    from komapy import set_api_key

    set_api_key('API_KEY')


Now you are ready to create a KomaPy chart. Here it is simple example to plot
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
which represent matplotlib subplots figure, and it holds information about
``series`` property for each figure. A ``series`` property represent matplotlib
``axis`` instance in KomaPy realm.

In a chart config, you can define one or more layout data, and one or more
series data. The default chart layout in KomaPy is column-based layout, but you
can use grid layout too.

The property ``'name': 'edm'`` tell KomaPy that it should fetch EDM data from
BMA API, and filtering is done using ``query_params`` data:

.. code-block:: python

    'query_params': {
        'benchmark': 'BAB0',
        'reflector': 'RB2',
        'start_at': '2019-04-01',
        'end_at': '2019-08-01',
        'ci': True
    },

The property ``fields`` is required and it tells KomaPy that it should plot
field named ``timestamp`` on x axis, and field named ``slope_distance`` on y
axis. The property ``xaxis_date`` tells that on x axis, it should be using
datetime value instead of regular value.
