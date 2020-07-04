Geting Data From Chart
======================

KomaPy provides several API to get data from chart. For example, consider the
following chart:

.. code-block:: python

    from komapy import Chart

    chart = Chart({
        'title': 'Get Data From Chart',
        'layout': {
            'data': [
                {
                    'series': {
                        'index': 'series-0',
                        'fields': [
                            [1, 2, 3],
                            [1, 2, 3],
                        ]
                    }
                },
                {
                    'series': {
                        'index': 'series-1',
                        'fields': [
                            [3, 4, 5],
                            [3, 4, 5],
                        ]
                    }
                },
            ]
        }
    })

    chart.render()

In the above example, we name the series using unique index, ``series-0`` for
the first series and ``series-1`` for the second series. To get series instance
(instance of ``komapy.series.Series``) we use ``Chart.get_series()`` method:

.. code-block:: python

    series = chart.get_series(index='series-0')

    print(series.index) # Output: series-0
    print(series.fields) # Output: [[1, 2, 3], [1, 2, 3]]

To get resolved data from series, call ``Chart.get_data()`` method:

.. code-block:: python

    data = chart.get_data(index='series-1')

    print(data) # Output: [[3, 4, 5], [3, 4, 5]]

If index is integer, it corresponds to the index in the series or data
container. For example, if index is 0 in the ``Chart.get_data()`` method, it
will find the first index of all data in the list:

.. code-block:: python

    data = chart.get_data(index=0)

    print(data) # Output: [[1, 2, 3], [4, 5, 6]]

If index is None, it will return all series or data container. For example, if
index is not provided the ``Chart.get_series()`` method, it will return all
series instance.
