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

fields
------

type: list, function

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

name
----

type: str

default: None

BMA API name like ``doas``, ``edm``, ``tiltmeter``, ``seismicity``, etc.

Example:

.. code-block:: python

    series = Series(name='seismicity')

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
