========================
KomaPy Series Properties
========================

Below is the list of available series properties. The only required property to
be set is ``fields`` property.

addons
------

type: list

default: []

Series plot addons. Each addons entry contains a dictionary of addons
configuration. The only required key is ``name``. Other keys left as optional
parameter and will be passed to particular addons resolver.

Example:

.. code-block:: python

    series = Series(
        addons=[
            {
                name: 'addon',
            }
        ]
    )

aggregations
------------

type: list

default: []

Series data aggregations. Data aggregation allows to manipulate plot data for
specific field without affecting another field before it get rendered into the
chart object. Each aggregations entry contains a dictionary of aggregation
configuration. Required key are ``func`` which is a name of aggregation function
and ``field`` which is name of data field the resolver should target. Other key
is ``params`` which is a dictionary argument that will be passed to the
aggregation resolver function.

Example:

.. code-block:: python

    series = Series(
        aggregations=[
            {
                'func': 'cumsum',
                'field': 'energy',
                'params: {

                }
            }
        ]
    )

axis
----

type: int

default: None

Axis index used to plot the current series. Axis index is measured from 0 at
current figure. For example, if you generate 2 series and want to plot the
second series on the same axis as the first series, you may want to use axis
index 0 because this axis is already generated.

csv_params
----------

type: dict

default: {}

CSV parameters to be passed to the CSV resolver. Default CSV resolver is
``pandas.read_csv``. So, all parameters will be passed as keyword arguments to
the pandas read_csv keyword arguments.

csv
---

type: str

default: None

Path to the CSV file or CSV URL.

Example:

.. code-block:: python

    series = Series(csv='http://api.example.com/data.csv')

excel_params
------------

.. versionadded:: 0.7.0

type: dict

default: {}

Excel parameters to be passed to the resolver. Default resolver is
``pandas.read_excel``. So, all parameters will be passed as keyword arguments to
the pandas read_excel keyword arguments.

excel
-----

.. versionadded:: 0.7.0

type: str

default: None

Path to the Excel file.

field_options
-------------

.. versionadded:: 0.2.0

type: dict

default: {}

Optional parameters to be passed to the ``fields`` if the type is a function.

Example:

.. code-block:: python

    def plot_series(axis, **options):
        if options.get('x'):
            # Do something with axis if value 'x' is in options.
        return axis

    series = Series(
        fields=plot_series,
        field_options={
            'x': 2,
            'y': 3
        }
    )

    # or set the field_options in the chart configuration

    config = {
        'layout': {
            'data': [
                {
                    'series': {
                        'fields': plot_series,
                        'field_options': {
                            'x': 2,
                            'y': 3
                        }
                    }
                }
            ]
        }
    }

fields
------

type: list, callable

default: []

Data fields to plot. If using CSV, JSON URL, or BMA API name, fields can be a
list of column name or JSON field name you want to plot. If you want to plot
timestamp vs energy, you can write the fields like this: ``['timestamp',
'energy']``.

Example:

.. code-block:: python

    series = Series(name='energy', fields=['timestamp', 'energy'])

formatter
---------

type: dict

default: {}

Axis formatter configuration. The parameters will be passed to the Matplotlib
axis formatter class.

Example:

.. code-block:: python

    series = Series(
        formatter={
            'x': {
                'major': {
                    'format': '%.3f'
                },
                'minor': {
                    'name': 'PercentFormatter',
                    'params': [],
                    'keyword_params': {

                    }
                }
            }
        }
    )

grid
----

type: dict

default: {}

Grid parameters used in grid layout.

TODO: Add example.

index
-----

.. versionadded:: 0.7.0

type: int | str

default: None

Unique index name to identify certain series. It is useful if you want to get
instance or data from the series. For example:

.. code-block:: python

    from komapy import Chart

    chart = Chart({
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

    series1 = chart.get_series(index='series-1')
    data1 = chart.get_data(index='series-1')

If index is integer, it corresponds to the index in the series or data
container. For example, if index is 0 in the ``Chart.get_series()`` method, it
will find the first index of all series in the list. On the other hand, if index
is string, it will find the series that match the index name.

If index is None, it will return all series or data container. For example, if
index is not provided the ``Chart.get_series()`` method, it will return all
series instance.

json_params
-----------

.. versionadded:: 0.7.0

type: dict

default: {}

JSON parameters to be passed to the JSON resolver. Default JSON resolver is
``pandas.read_json``. So, all parameters will be passed as keyword arguments to
the pandas read_json keyword arguments.

json
----

.. versionadded:: 0.7.0

type: str

default: None

Path to JSON file or JSON URL.

labels
------

type: dict

default: {}

Axis label configuration. The parameters will be passed to the Matplotlib axis
``set_xlabel`` or ``set_ylabel`` methods.

Example:

.. code-block:: python

    series = Series(
        labels={
            'x': {
                'text': 'x'
                'style': {

                }
            }
        }
    )

legend
------

type: dict

default: {}

Axis legend configuration. The parameters will be passed to the Matplotlib axis
legend method. The only required parameter is ``show`` which is a boolean value
indicating the legend should be drawn or not.

Example:

.. code-block:: python

    series = Series(
        legend={
            'show': True,
            'loc: 'upper left'
        }
    )

locator
-------

type: dict

default: {}

Axis locator configuration. The parameters will be passed to the Matplotlib axis
locator class.

Example:

.. code-block:: python

    series = Series(
        locator={
            'x': {
                'major': {
                    'name': 'MaxNLocator',
                    'params': [],
                    'keyword_params': {

                    }
                }
            }
        }
    )

merge_options
-------------

.. versionadded:: 0.5.0

type: dict

default: {}

Merge options when using series partial. All arguments will be passed to the
Pandas DataFrame append function.

name
----

type: str

default: None

BMA API name like ``doas``, ``edm``, ``tiltmeter``, ``seismicity``, etc.

Example:

.. code-block:: python

    series = Series(name='seismicity')

partial
-------

.. versionadded:: 0.5.0

type: list

default: []

Series partial configuration. It is useful if you want to fetch data in partial
or using multiple data resolvers. For example, fetching BMA data in different
timespan, but you want to plot in a single figure.

Example:

.. code-block:: python

    series = Series(
        partial=[
            {
                'name': 'edm',
                'query_params': {
                    'timestamp__gte': '2011-01-01',
                    'timestamp__lt': '2019-03-01',
                    'benchmark': 'BAB0',
                    'reflector': 'RB2',
                    'nolimit': True,
                }
            },
            {
                'name': 'edm',
                'query_params': {
                    'start_at': '2019-03-01',
                    'end_at': '2020-01-01',
                    'benchmark': 'BAB0',
                    'reflector': 'RB2',
                    'ci': True,
                }
            },
        ])

Data from multiple queries in the partial entries will be appended into a single
DataFrame object. In the above example, we fetch BMA EDM data in different
timespan, and using different query parameters. Because we have the same query
name (``edm``), columns with the same name will be appended into a single
DataFrame object. Note that query ordering matters.

Note that using multiple queries with different plot name will result in
undefined behaviour.

plot_params
-----------

type: dict

default: {}

Axis plot parameters. The parameters will be passed to the particular plot
resolver. You may want to set the parameters to customize series style like
marker, marker size, plot color, etc.

Example:

.. code-block::

    series = Series(
        plot_params={
            'color': 'k',
            'marker': 'o',
            'markersize': 6,
            'zorder': 2,
            'linewidth': 1,
            'label': 'RB2',
        }
    )

query_params
------------

type: dict

default: {}

URL query parameters. The parameters will be used as field query filtering for
BMA API name or URL query parameters.

Example:

.. code-block:: python

    series = Series(
        name='edm',
        query_params={
            'benchmark: 'BAB0',
            'reflector': 'RB2',
            'start_at': '2019-04-01',
            'end_at: '2019-08-01',
            'ci': True
        }
    )

secondary
---------

type: str

default: None

Name of axis to build secondary axis. Accepted name are ``x`` for x axis, and
``y`` for y axis.

Example:

.. code-block:: python

    series = Series(secondary='x')

sql_params
----------

.. versionadded:: 0.7.0

type: dict

default: {}

SQL parameters to be passed to the resolver. Default resolver is
``pandas.read_sql``. So, all parameters will be passed as keyword arguments to
the pandas read_sql keyword arguments.

sql
---

.. versionadded:: 0.7.0

type: list

default: []

SQL query and database information to be passed to the resolver. The first
element in the list must be SQL query to be executed, and the second element
must be SQLAlchemy connectable (engine/connection). For example:

.. code-block:: python

    from sqlalchemy import create_engine

    engine = create_engine('sqlite://./db.sqlite3')
    query = "select `timestamp`, `slope_distance` from `rb2` order by `timestamp` asc"
    sql = [query, engine]

tertiary
--------

.. versionadded:: 0.4.0

type: dict

default: {}

Options to plot series on tertiary axis.

Example:

.. code-block:: python

    series = Series(tertiary={
        'on': 'x',
        'side': 'right',
        'position': ('outward', 60)
    })

The example above will create a tertiary axis on x axis, and the axis spine
right side will be moved outward by 60 points.

See available options below to customize tertiary axis.

on
~~

type: str

default: x

Name of axis to twin it. If you set to ``x``, you use x axis as shared axis,
Otherwise, if you set to ``y``, you use y axis as shared axis.

side
~~~~

type: str

default: right

On which axis spine side to apply modification. Typical values are ``left``
and ``right``.

position
~~~~~~~~

type: str, tuple

default: 'zero'

Set axis spine position. The value will be passed to the Matplotlib axis spine
``set_position`` method.

title
-----

Series title name.

Example:

.. code-block:: python

    series = Series(title='RB2')

transforms
----------

type: list

default: []

Series data transformations. Data transformation allows changes to the plot data
before it rendered into the chart object. Some example is to transfrom EDM data
to apply slope distance correction after data had been resolved.

Each entry contains a function of data transformation, or a string if the
function has been registered to the KomaPy data transformation registers.

Example:

.. code-block:: python

    series = Series(
        transforms=[
            'slope_correction'
        ]
    )

type
----

type: str

default: line

Name of series plot type. Default value is line plot. Accepted values include
bar, errorbar, scatter, etc.

Example:

.. code-block:: python

    series = Series(type='bar')

url
---

A URL that returns JSON data. KomaPy will fetch the data from the URL and use it
as data source.

Example:

.. code-block:: python

    series = Series(
        url='http://cendana15.com/api/analytics/edm?start_at=2019-04-01&end_at=2019-08-01'
    )

xaxis_date
----------

type: boolean

default: False

Tells if the x axis should be using datetime format or not. KomaPy will convert
the value to the datetime value.

Example:

.. code-block:: python

    series = Series(xaxis_date=True)

yaxis_date
----------

type: boolean

default: False

Tells if the y axis should be using datetime format or not. KomaPy will
convert the value to the datetime value.

Example:

.. code-block:: python

    series = Series(yaxis_date=True)
