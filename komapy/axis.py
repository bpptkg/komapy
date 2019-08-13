from functools import partial
from functools import lru_cache
from collections import OrderedDict

import matplotlib.ticker

from . import processing
from . import client
from . import utils

from .exceptions import ChartError
from .constants import SUPPORTED_CUSTOMIZERS


def set_axis_locator(axis, on='x', which='major', params=None):
    """Set axis locator."""
    config = params or {}
    methods = {
        'x': 'get_xaxis',
        'y': 'get_yaxis',
        'major': 'set_major_locator',
        'minor': 'set_minor_locator',
    }

    locator = getattr(matplotlib.ticker, config.get('name', ''), None)
    if locator:
        gca = getattr(axis, methods[on])
        getattr(gca, methods[which])(locator(**config.get('params', {})))


def set_axis_formatter(axis, on='x', which='major', params=None):
    """Set axis formatter."""
    config = params or {}
    methods = {
        'x': 'get_xaxis',
        'y': 'get_yaxis',
        'major': 'set_major_formatter',
        'minor': 'set_minor_formatter,'
    }

    supported_formatter = [
        'FormatStrFormatter',
        'StrMethodFormatter',
    ]

    name = config.get('name')
    if name:
        if name not in supported_formatter:
            raise ChartError('Unsupported formatter {}'.format(name))
    else:
        return

    formatter = getattr(matplotlib.ticker, name, None)
    if formatter:
        gca = getattr(axis, methods[on])
        getattr(gca, methods[which])(formatter(config.get('format')))


def set_axis_legend(axis, params=None):
    """Set axis legend."""
    config = params or {}

    if config.pop('show', False):
        axis.legend(**config)


def set_axis_label(axis, which='x', params=None):
    """Set axis label."""
    config = params or {}

    methods = {
        'x': 'set_xlabel',
        'y': 'set_ylabel',
    }

    method = getattr(axis, methods[which], None)
    method(config.get('text'), **config.get('style', {}))


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
        if source:
            index = config.fields.index(agg_field)
        func = config.aggregation.get('func', [])
        if not func:
            return plot_data

        for item in func:
            for name, params in item.items():
                if name in processing.SUPPORTED_AGGREGATIONS:
                    method = getattr(
                        processing, processing.SUPPORTED_AGGREGATIONS[name])
                    plot_data[index] = method(plot_data[index], params)

    return plot_data
