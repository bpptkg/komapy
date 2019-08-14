"""
Matplotlib axes customization wrapper.
"""

from functools import partial
from functools import lru_cache
from collections import OrderedDict, Callable

import matplotlib.ticker

from . import processing
from . import client
from . import transforms
from . import utils

from .constants import SUPPORTED_CUSTOMIZERS
from .exceptions import ChartError


def set_axis_locator(axis, params=None):
    """
    Set axis locator.

    Example config:

        'locator': {
            'x': {
                'major': {
                    'name': 'MaxNLocator',
                    'params': [],
                    'keyword_params': {

                    } 
                }
            }
        }
    """
    config = params or {}
    axis_methods = {
        'x': 'get_xaxis',
        'y': 'get_yaxis',
    }
    formatter_methods = {
        'major': 'set_major_locator',
        'minor': 'set_minor_locator',
    }
    supported_locator = [
        'AutoLocator',
        'MaxNLocator',
        'LinearLocator',
        'LogLocator',
        'MultipeLocator',
        'FixedLocator',
        'IndexLocator',
        'NullLocator',
        'SymmetricalLocator',
        'LogitLocator',
        'OldAutoLocator',
        'AutoMinorLocator',
    ]

    for key, value in config.items():
        if key not in axis_methods:
            continue
        for which, data in value.items():
            if which not in formatter_methods:
                continue
            name = data.get('name')
            if name not in supported_locator:
                continue
            locator = getattr(matplotlib.ticker, data.get('name', ''), None)
            if locator:
                gca = getattr(axis, axis_methods[key])()
                getattr(gca, formatter_methods[which])(
                    locator(*data.get('params', []),
                            **data.get('keyword_params', {}))
                )


def set_axis_formatter(axis, params=None):
    """
    Set axis formatter.

    Example config:

        'formatter': {
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

    Default formatter is FormatStrFormatter and it reads 'format' value. Other
    formatter is specified with params and keyword_params to pass these values
    into formatter class.
    """
    config = params or {}
    axis_methods = {
        'x': 'get_xaxis',
        'y': 'get_yaxis',
    }
    formatter_methods = {
        'major': 'set_major_formatter',
        'minor': 'set_minor_formatter,'
    }
    supported_formatter = {
        'NullFormatter',
        'IndexFormatter',
        'FixedFormatter',
        'FuncFormatter',
        'StrMethodFormatter',
        'FormatStrFormatter',
        'ScalarFormatter',
        'LogFormatter',
        'LogFormatterExponent',
        'LogFormatterMathText',
        'LogFormatterSciNotation',
        'LogitFormatter',
        'EngFormatter',
        'PercentFormatter',
    }

    for key, value in config.items():
        if key not in axis_methods:
            continue
        gca = getattr(axis, axis_methods[key])()
        for which, data in value.items():
            if which in formatter_methods:
                name = data.get('name', 'FormatStrFormatter')
                if name not in supported_formatter:
                    continue
                formatter = getattr(matplotlib.ticker, name)
                if name in ['FormatStrFormatter', 'StrMethodFormatter']:
                    getattr(gca, formatter_methods[which])(
                        formatter(data.get('format')))
                else:
                    getattr(gca, formatter_methods[which])(
                        formatter(*data.get('params', []),
                                  **data.get('keyword_params', {}))
                    )


def set_axis_legend(axis, params=None):
    """Set axis legend."""
    config = params or {}

    if config.pop('show', False):
        axis.legend(**config)


def set_axis_label(axis, params=None):
    """
    Set axis label.

    Example config:

        'labels': {
            'x': {
                'text': 'x'
                'style': {

                }
            }
        }
    """
    config = params or {}

    methods = {
        'x': 'set_xlabel',
        'y': 'set_ylabel',
    }

    for key, value in config.items():
        if key not in methods:
            continue
        method = getattr(axis, methods[key])
        method(value.get('text', ''), **value.get('style', {}))


def build_secondary_axis(axis, on='x'):
    """Build twin secondary axis."""
    methods = {
        'x': 'twinx',
        'y': 'twiny',
    }
    method = getattr(axis, methods[on])
    return method()


def customize_axis(axis, params):
    """
    Customize axis based-on given params.
    """
    config = params.copy()

    for name in config:
        if name in SUPPORTED_CUSTOMIZERS:
            modifier = config[name]
            if isinstance(modifier, dict):
                value = modifier.pop('value', None)
                if isinstance(value, list):
                    args = [value]
                else:
                    args = []

                kwargs = modifier
            elif isinstance(modifier, list):
                args = list(modifier)
                kwargs = {}
            else:
                args = [modifier]
                kwargs = {}

            method_name = getattr(axis, SUPPORTED_CUSTOMIZERS[name])
            customizer = partial(method_name, *args, **kwargs)
            customizer()


@lru_cache(maxsize=128)
def resolve_data(config):
    """
    Resolve plot data.

    Plot data is resolved in the following order, CSV, JSON URL, and BMA API
    name. Each of sources has certain resolver. If none of the sources found
    in the chart config, data source is treated as plain object.
    """
    sources = OrderedDict([
        ('csv', {
            'resolver': processing.read_csv,
            'options': 'csv_options'
        }),
        ('url', {
            'resolver': client.fetch_url_as_dataframe,
            'options': 'query_params'
        }),
        ('name', {
            'resolver': client.fetch_bma_as_dataframe,
            'options': 'query_params'
        }),
    ])

    for name in sources:
        source = getattr(config, name, None)
        if source:
            resolve = sources[name]['resolver']
            options = getattr(config, sources[name]['options'], {})
            break

    if source:
        resource = resolve(source, options)
        func = partial(processing.dataframe_or_empty, resource)
        iterator = map(func, config.fields)
    else:
        iterator = config.fields

    plot_data = []
    for i, field in enumerate(iterator):
        if i == 0 and config.xaxis_date:
            plot_data.append(utils.resolve_timestamp(field))
        elif i == 1 and config.yaxis_date:
            plot_data.append(utils.resolve_timestamp(field))
        else:
            plot_data.append(field)

    agg_field = config.aggregation.pop('on', None)
    index = agg_field
    if agg_field:
        func = config.aggregation.get('func', [])
        if not func:
            return plot_data
        if source:
            index = config.fields.index(agg_field)

        for item in func:
            for name, callable_or_params in item.items():
                if name in processing.SUPPORTED_AGGREGATIONS:
                    method = getattr(
                        processing, processing.SUPPORTED_AGGREGATIONS[name])
                    plot_data[index] = method(
                        plot_data[index], callable_or_params)
                else:
                    method = callable_or_params
                    if not callable(method):
                        continue
                    plot_data[index] = method(plot_data[index])

    if config.transform:
        for callback in config.transform:
            if isinstance(callback, str):
                if callback in transforms.SUPPORTED_TRANSFORMS:
                    callback = getattr(transforms, callback)
                    plot_data = callback(plot_data, config)
            elif isinstance(callback, Callable):
                plot_data = callback(plot_data, config)

    return plot_data
