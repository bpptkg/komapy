================
Data Aggregation
================

Data aggregation allows to manipulate plot data for specific field without
affecting another field before it get rendered into the chart object. Some
example include computing cumulative sum, multiplying data with a constant
factor, etc. See the following example:

.. code-block:: python

    from komapy import Chart

    series = {
        'name': 'energy',
        'query_params': {
            'eventdate__gte': '2019-04-01',
            'eventdate__lt': '2019-08-01',
            'eventtype__in': 'VTA,VTB,MP',
            'accumulate': True,
            'nolimit': True
        },
        'fields': ['timestamp', 'energy'],
        'xaxis_date': True,
        'aggregations': [
            {
                'func': 'cumsum',
                'field': 'energy',
                'params': {

                }
            }
        ]
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

Data aggregation contains a list of dictionary entry of aggregation function.
Aggregation ``func`` is the name of aggregation function. If its type equal to
string, KomaPy will assume that it is a built-in aggregation function. You can
set it to the some callbable function to build your custom aggreation function.
Aggregation ``field`` is required to tell KomaPy on what data field the callback
should target. This can be a name of data field in the ``fields`` list or
integer index if you use plain data. You can specify optional callback
parameters in ``params``. Here it is an example of cumulative sum aggregation
function:

.. code-block:: python

    def cumsum(data, params=None):
        """Cumulative sum function aggregation."""
        kwargs = params or {}
        return data.cumsum(**kwargs)

The function is pretty simple. It just take ``data`` argument and an optional
``params`` argument. The function returns cumulative sum of data. In the above
example, we set aggregation field to ``energy``, so the ``data`` argument in the
aggreation function will be energy data.
