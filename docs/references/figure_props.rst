========================
KomaPy Figure Properties
========================

title
-----

type: str

default: None

A chart title.

Example:

.. code-block:: python

    from komapy import Chart

    chart = Chart({
        'title': 'Seismicity'
    })
    chart.render()
    chart.save('figure.png')


theme
-----

type: str

default: None

Matplotlib plot style to use. All style names can be found using this simple
snippet:

.. code-block:: python

    import matplotlib.pyplot as plt

    print(plt.style.available)

Example:

.. code-block:: python

    from komapy import Chart

    chart = Chart({
        'theme': 'seaborn'
    })
    chart.render()
    chart.save('figure.png')


timezone
--------

type: str

default: Asia/Jakarta

Default time zone location name used in the chart. This field particularly used
to convert non-aware datetime to timezone-aware datetime in the extensions plot.

Example:

.. code-block:: python

    from komapy import Chart

    chart = Chart({
        'timezone': 'Asia/Jakarta',
        'theme': 'seaborn',
        'layout': {
            'data': [
                {
                    'series': {
                        'type': 'bar',
                        'name': 'seismicity',
                        'query_params': {
                            'eventdate__gte': '2018-05-01',
                            'eventdate__lt': '2018-11-01',
                            'eventtype': 'MP',
                            'nolimit': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'label': 'MP'
                        },
                        'fields': ['timestamp', 'count'],
                        'xaxis_date': True,
                    }
                }
            ]
        },
        'extensions': {
            'starttime': '2018-05-01',
            'endtime': '2018-11-01',
            'plot': [
                {
                    'name': 'dome',
                    'label': 'Kubah lava tampak'
                }
            ]
        }
    })
    chart.render()
    chart.save('figure.png')


layout
------

type: dict

default: {}

Chart layout configuration. Chart layout acts as a figure container. It holds
chart subplots, series entries, grid configuration, etc. See the following of
all available chart layout properties.


type
^^^^

type: str

default: default

Chart layout type. KomaPy support two layout type, i.e. row oriented
(``default``) and grid oriented (``grid``) layouts.

Example:

.. code-block:: python

    from komapy import Chart

    chart = Chart({
        'layout': {
            'type': 'grid',
            ...
        }
    })
    chart.render()
    chart.save('figure.png')


size
^^^^

type: list, sequence of two integers

default: []

Chart layout size. It's only applied to grid layout type.

Example:

.. code-block:: python

    from komapy import Chart

    chart = Chart({
        'layout': {
            'type': 'grid',
            'size': [2, 2],
            ...
        }
    })
    chart.render()
    chart.save('figure.png')


options
^^^^^^^

type: dict

default: {}

Chart layout options. This is particularly used to customize subplot or grid
layout.

Example:

.. code-block:: python

    from komapy import Chart

    chart = Chart({
        'layout': {
            'options': {
                'sharex': True,
                'figsize': [12, 6]
            },
            ...
        }
    })
    chart.render()
    chart.save('figure.png')


data
^^^^

type: list

default: []

Chart layout entries. It is where a subplot entry is added. Each entry represent
a subplot figure. Each subplot entry must be a dictionary type.

Example:

.. code-block:: python

    from komapy import Chart

    chart = Chart({
        'theme': 'seaborn',
        'layout': {
            'options': {
                'sharex': True,
                'figsize': [12, 4]
            },
            'data': [
                {
                    'series': {
                        'type': 'bar',
                        'name': 'seismicity',
                        'query_params': {
                            'eventdate__gte': '2018-05-01',
                            'eventdate__lt': '2018-11-01',
                            'eventtype': 'MP',
                            'nolimit': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'label': 'MP'
                        },
                        'fields': ['timestamp', 'count'],
                        'xaxis_date': True,
                    }
                },
                {
                    'series': {
                        'type': 'bar',
                        'name': 'seismicity',
                        'query_params': {
                            'eventdate__gte': '2018-05-01',
                            'eventdate__lt': '2018-11-01',
                            'eventtype': 'LF',
                            'nolimit': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'label': 'LF'
                        },
                        'fields': ['timestamp', 'count'],
                        'xaxis_date': True,
                    }
                }
            ]
        }
    })
    chart.render()
    chart.save('figure.png')


figure_options
--------------

type: dict

default: {}

Matplotlib figure options. All entries are passed to the Matplotlib
``plt.figure()`` function.

You can see Matplotlib figure documentation for comprehensize list of all
available parameters.


save_options
------------

type: dict

default: {}

Matplotlib save figure options. All entries are passed to the Matplotlib
``plt.savefig()`` function.


tight_layout
------------

type: dict

default: {}

Matplotlib tight layout options. All entries are passed to the Matplotlib
``plt.tight_layout()`` function.


extensions
----------

type: dict

default: {}

Extension plot configuration. It is a feature to accommodate non-series data
plot in a chart object. Each extension plot entry is will be rendered on each
subplot or axis. See the following of all available extension properties.


starttime
^^^^^^^^^

type: str

default: None

required: True

Date time indicating start time of extension plot.

Example:

.. code-block:: python

    from komapy import Chart

    chart = Chart({
        'theme': 'seaborn',
        'layout': {
            'data': [
                {
                    'series': {
                        'type': 'bar',
                        'name': 'seismicity',
                        'query_params': {
                            'eventdate__gte': '2018-05-01',
                            'eventdate__lt': '2018-11-01',
                            'eventtype': 'MP',
                            'nolimit': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'label': 'MP'
                        },
                        'fields': ['timestamp', 'count'],
                        'xaxis_date': True,
                    }
                }
            ]
        },
        'extensions': {
            'starttime': '2018-05-01',
            'endtime': '2018-11-01',
            'plot': [
                {
                    'name': 'dome',
                    'label': 'Kubah lava tampak'
                }
            ]
        }
    })
    chart.render()
    chart.save('figure.png')


endtime
^^^^^^^

type: str

default: None

required: True

Date time indicating end time of extension plot.

Example:

.. code-block:: python

    from komapy import Chart

    chart = Chart({
        'theme': 'seaborn',
        'layout': {
            'data': [
                {
                    'series': {
                        'type': 'bar',
                        'name': 'seismicity',
                        'query_params': {
                            'eventdate__gte': '2018-05-01',
                            'eventdate__lt': '2018-11-01',
                            'eventtype': 'ROCKFALL',
                            'nolimit': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'label': 'RF'
                        },
                        'fields': ['timestamp', 'count'],
                        'xaxis_date': True,
                    }
                }
            ]
        },
        'extensions': {
            'starttime': '2018-05-01',
            'endtime': '2018-11-01',
            'plot': [
                {
                    'name': 'dome',
                    'label': 'Kubah lava tampak'
                }
            ]
        }
    })
    chart.render()
    chart.save('figure.png')


plot
^^^^

Extension plot entries. Each entry entry will be rendered on each subplot
figure. Each entry must be a dictionary type.

Example:

.. code-block:: python

    from komapy import Chart

    chart = Chart({
        'theme': 'seaborn',
        'layout': {
            'data': [
                {
                    'series': {
                        'type': 'bar',
                        'name': 'seismicity',
                        'query_params': {
                            'eventdate__gte': '2018-05-01',
                            'eventdate__lt': '2018-11-01',
                            'eventtype': 'ROCKFALL',
                            'nolimit': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'label': 'RF'
                        },
                        'fields': ['timestamp', 'count'],
                        'xaxis_date': True,
                    }
                }
            ]
        },
        'extensions': {
            'starttime': '2018-05-01',
            'endtime': '2018-11-01',
            'plot': [
                {
                    'name': 'explosion',
                    'label': 'Letusan',
                    'color': 'red'
                },
                {
                    'name': 'dome',
                    'label': 'Kubah lava tampak'
                }
            ]
        }
    })
    chart.render()
    chart.save('figure.png')

This will draw explosion line and dome appearance line on each subplot figure.

legend
^^^^^^

Extension plot legend configuration. All entries will be passed to the
Matplotlib figure instance legend function.

Example:

.. code-block:: python

    from komapy import Chart

    chart = Chart({
        'theme': 'seaborn',
        'layout': {
            'data': [
                {
                    'series': {
                        'type': 'bar',
                        'name': 'seismicity',
                        'query_params': {
                            'eventdate__gte': '2018-05-01',
                            'eventdate__lt': '2018-11-01',
                            'eventtype': 'ROCKFALL',
                            'nolimit': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'label': 'RF'
                        },
                        'fields': ['timestamp', 'count'],
                        'xaxis_date': True,
                    }
                }
            ]
        },
        'extensions': {
            'starttime': '2018-05-01',
            'endtime': '2018-11-01',
            'plot': [
                {
                    'name': 'explosion',
                    'label': 'Letusan',
                    'color': 'red'
                },
                {
                    'name': 'dome',
                    'label': 'Kubah lava tampak'
                }
            ],
            'legend': {
                'show': True,
                'loc': 'lower center',
                'ncol': 2,
                'frameon': False,
                'fancybox': False
            }
        }
    })
    chart.render()
    chart.save('figure.png')

You have to pass ``show`` field to actually show the legend in the chart figure.


use_cache
---------

type: bool

default: False

Cache the resource query or not. It is useful if you have a same resource query
and you use it in the different series or subplot. Instead of querying the same
JSON data for example, KomaPy will fetch the JSON data only once, and use it through out a
chart. Series field data will be extracted from the resource cache.

Example:

.. code-block:: python

    from komapy import Chart

    chart = Chart({
        'use_cache': True,
        'layout': {
            'data': [
                {
                    'series': {
                        'name': 'tiltmeter',
                        'query_params': {
                            'timestamp__gte': '2019-10-01',
                            'timestamp__lt': '2019-11-01',
                            'station': 'selokopo',
                            'nolimit': True
                        },
                        'plot_params': {
                            'zorder': 2,
                            'label': 'X'
                        },
                        'fields': ['timestamp', 'x'],
                        'xaxis_date': True,
                    }
                },
                {
                    'series': {
                        'name': 'tiltmeter',
                        'query_params': {
                            'timestamp__gte': '2019-10-01',
                            'timestamp__lt': '2019-11-01',
                            'station': 'selokopo',
                            'nolimit': True
                        },
                        'plot_params': {
                            'zorder': 2,
                            'label': 'Y'
                        },
                        'fields': ['timestamp', 'y'],
                        'xaxis_date': True,
                    }
                },
                {
                    'series': {
                        'name': 'tiltmeter',
                        'query_params': {
                            'timestamp__gte': '2019-10-01',
                            'timestamp__lt': '2019-11-01',
                            'station': 'selokopo',
                            'nolimit': True
                        },
                        'plot_params': {
                            'zorder': 2,
                            'label': 'Temperature'
                        },
                        'fields': ['timestamp', 'temperature'],
                        'xaxis_date': True,
                    }
                },
            ]
        }
    })
    chart.render()
    chart.save('figure.png')

You can see in the above example, we query the same tiltmeter data for each
series and subplot. By using cache, KomaPy will fetch tiltmeter data only once.
Field name ``x``, ``y``, and ``temperature`` will be extracted from cache, i.e.
JSON data fetched in the first query.


rc_params
---------

.. versionadded:: 0.3.0

type: dict

default: {}

Matplotlib rcParams configuration. All entries will be passed to the
``plt.rcParams.update()`` function. This is useful if you want to customize
default Matplotlib rcParams variable.

Example:

.. code-block:: python

    from komapy import Chart

    chart = Chart({
        'theme': 'seaborn',
        'rc_params': {
            'font.size': 14,
            'font.sans-serif': ['Helvetica']
        },
        'layout': {
            'options': {
                'sharex': True,
                'figsize': [12, 4]
            },
            'data': [
                {
                    'series': {
                        'type': 'bar',
                        'name': 'seismicity',
                        'query_params': {
                            'eventdate__gte': '2018-05-01',
                            'eventdate__lt': '2018-11-01',
                            'eventtype': 'MP',
                            'nolimit': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'label': 'MP'
                        },
                        'fields': ['timestamp', 'count'],
                        'xaxis_date': True,
                    }
                },
                {
                    'series': {
                        'type': 'bar',
                        'name': 'seismicity',
                        'query_params': {
                            'eventdate__gte': '2018-05-01',
                            'eventdate__lt': '2018-11-01',
                            'eventtype': 'LF',
                            'nolimit': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'label': 'LF'
                        },
                        'fields': ['timestamp', 'count'],
                        'xaxis_date': True,
                    }
                }
            ]
        }
    })
    chart.render()
    chart.save('figure.png')
