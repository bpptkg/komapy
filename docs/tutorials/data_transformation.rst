===================
Data Transformation
===================

Data transformation allows changes to the plot data before it rendered into the
chart object. Some example is to transfrom EDM data to apply slope distance
correction after data had been resolved. You can specify one or more
transformation functions in the list. KomaPy will apply the transformation
function in the order.

Input argument for transformation function is resolved ``data`` (a list of plot
data with type of Pandas DataFrame) and series ``config``. The function returns
a list of transformed plot data.

Here it the example of transformation function to apply EDM slope distance
correction:

.. code-block:: python

    import pandas as pd
    from komapy.client import fetch_bma_as_dataframe

    def slope_correction(data, config):
        """
        Apply EDM slope distance correction.
        """
        if config.name != 'edm':
            return data

        timestamp__gte = config.query_params.get(
            'timestamp__gte') or config.query_params.get('start_at')
        timestamp__lt = config.query_params.get(
            'timestamp__lt') or config.query_params.get('end_at')

        err_data = fetch_bma_as_dataframe('slope', {
            'timestamp__gte': timestamp__gte,
            'timestamp__lt': timestamp__lt,
            'benchmark': config.query_params['benchmark'],
            'reflector': config.query_params['reflector'],
        })
        if err_data.empty:
            return data

        slope_data = pd.DataFrame()
        for item in data:
            slope_data.join(item)

        corrected_data = slope_data.apply(
            lambda item: item.slope_distance + err_data.where(
                err_data.timestamp > item.timestamp).deviation.sum(), axis=1)
        return [data[0], corrected_data]


Then add that transformation function to series config:

.. code-block:: python

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
        'xaxis_date': True,
        'transforms': [
            slope_correction,
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
