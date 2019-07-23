import re
import copy

from functools import partial
from collections import OrderedDict
from cached_property import cached_property

import matplotlib.pyplot as plt
import matplotlib.ticker
import matplotlib.gridspec as gridspec

from pandas.plotting import register_matplotlib_converters

from . import client
from . import extensions
from . import processing
from . import utils
from .exceptions import ChartError

register_matplotlib_converters()

SUPPORTED_NAMES = [
    'doas',
    'edm',
    'gas_emission',
    'gas_temperature',
    'gps_position',
    'gps_baseline',
    'rsam_seismic',
    'rsam_seismic_band',
    'rsam_infrasound',
    'rsam_seismic_band',
    'thermal',
    'tiltmeter',
    'tiltmeter_raw',
    'tiltborehole',
    'seismicity',
    'bulletin',
    'energy',
    'magnitude',
]

SUPPORTED_TYPES = {
    # Basic plotting
    'line': 'plot',
    'plot': 'plot',
    'errorbar': 'errorbar',
    'plot_date': 'plot_date',
    'step': 'step',
    'log': 'loglog',
    'loglog': 'loglog',
    'semilogx': 'semilogx',
    'semilogy': 'semilogy',
    'bar': 'bar',
    'barh': 'barh',
    'stem': 'stem',
    'eventplot': 'eventplot',

    # Spectral plotting
    'acorr': 'acorr',
    'angle_spectrum': 'angle_spectrum',
    'cohere': 'cohere',
    'csd': 'csd',
    'magnitude_spectrum': 'magnitude_spectrum',
    'phase_spectrum': 'phase_spectrum',
    'psd': 'psd',
    'specgram': 'specgram',
    'xcorr': 'xcorr',
}

SUPPORTED_CUSTOMIZERS = {
    # Appearance
    'grid': 'grid',
    'axis_off': 'set_axis_off',
    'axis_on': 'set_axis_on',
    'frame': 'set_frame_on',
    'axis_below': 'set_axisbelow',
    'facecolor': 'set_facecolor',

    # Property cycle
    'prop_cycle': 'set_prop_cycle',

    # Axis limits and direction
    'invert_xaxis': 'invert_xaxis',
    'invert_yaxis': 'invert_yaxis',
    'xlimit': 'set_xlim',
    'ylimit': 'set_ylim',
    'xbound': 'set_xbound',
    'ybound': 'set_ybound',

    # Axis labels, title, legends
    'xlabel': 'set_xlabel',
    'ylabel': 'set_ylabel',
    'title': 'set_title',
    'legend': 'legend',

    # Axis scales
    'xscale': 'set_xscale',
    'yscale': 'set_yscale',

    # Autoscaling and margins
    'margins': 'margins',
    'xmargin': 'set_xmargin',
    'ymargin': 'set_ymargin',
    'relim': 'relim',
    'autoscale': 'autoscale',
    'autoscale_view': 'autoscale_view',
    'autoscale_on': 'set_autoscale_on',
    'autoscalex_on': 'set_autoscalex_on',
    'autoscaley_on': 'set_autoscaley_on',

    # Aspect ratio
    'aspect': 'set_aspect',
    'adjustable': 'set_adjustable',

    # Ticks and tick labels
    'xticks': 'set_xticks',
    'xticklabels': 'set_xticklabels',
    'yticks': 'set_yticks',
    'yticklabels': 'set_yticklabels',
    'minorticks_off': 'minorticks_off',
    'minorticks_on': 'minorticks_on',
    'ticklabel_format': 'ticklabel_format',
    'tick_params': 'tick_params',
    'locator_params': 'locator_params',

    # Axis position
    'ancor': 'set_anchor',
    'position': 'set_position',

    # Async/Event based
    'callback': 'add_callback',

    # General artist properties
    'agg_filter': 'set_agg_filter',
    'alpha': 'set_alpha',
    'animated': 'set_animated',
    'clip_on': 'set_clip_on',
    'gid': 'set_gid',
    'label': 'set_label',
    'rasterized': 'set_rasterized',
    'sketch_params': 'set_sketch_params',
    'snap': 'set_snap',
    'artist_url': 'set_url',
    'zorder': 'set_zorder',
}


def apply_theme(name):
    """Apply matplotlib plot theme."""
    if name in plt.style.available:
        plt.style.use(name)


def get_validation_methods(root_class):
    """Get all validation metods in the root class."""
    re_validate_template = re.compile(r'validate_(?P<name>\w+)')

    validation_methods = []
    for item in root_class.__dict__:
        matched = re_validate_template.match(item)
        if matched:
            name = matched.groupdict().get('name')
            method_name = 'validate_{}'.format(name)
            validation_methods.append(method_name)

    return validation_methods


class SeriesConfig(object):
    """A series config object."""

    required_parameters = ['fields']
    _available_parameters = {
        'name': None,
        'query_params': {},
        'fields': [],
        'plot_params': {},
        'labels': {},
        'locator': {},
        'formatter': {},
        'aggregation': {},
        'secondary': None,
        'legend': {},
        'title': None,
        'type': 'line',
        'xaxis_date': False,
        'yaxis_date': False,
        'url': None,
        'csv': None,
        'csv_params': {},
        'grid': {},
    }

    def __init__(self, **kwargs):
        for key, value in self._available_parameters.items():
            if key in kwargs:
                setattr(self, key, kwargs[key])
            else:
                setattr(self, key, value)

        self._check_required_parameters(kwargs)

    def _check_required_parameters(self, kwargs):
        for param in self.required_parameters:
            if param not in kwargs:
                raise ChartError('Parameter {} is required'.format(param))

    def validate_name(self):
        """Validate name attribute."""
        if self.name:
            if self.name not in SUPPORTED_NAMES:
                raise ChartError('Unknown parameter name {}'.format(self.name))

    def validate_type(self):
        """Validate type attribute."""
        if self.type not in SUPPORTED_TYPES:
            raise ChartError('Unsupported plot type {}'.format(self.name))

    def validate_fields(self):
        """Validate fields attribute."""
        if not self.fields:
            raise ChartError('Series fields must be set')

    def validate(self):
        """Validate all config attributes."""
        validation_methods = get_validation_methods(SeriesConfig)

        for method in validation_methods:
            getattr(self, method)()


class LayoutConfig(object):
    """A layout config object."""

    def __init__(self, **kwargs):
        self.type = kwargs.get('type', 'default')
        self.size = kwargs.get('size', [])
        self.data = kwargs.get('data', [])
        self.options = kwargs.get('options', {})

    def validate_size(self):
        """Validate layout size attribute."""
        if self.type == 'grid':
            if not self.size:
                raise ChartError(
                    "Layout size must be set "
                    "if layout type is 'grid'")

            if len(self.size) != 2:
                raise ChartError('Layout size length must be 2')

    def validate_data(self):
        """Validate layout data attribute."""
        if self.type == 'grid':
            for layout in self.data:
                grid = layout.get('grid')
                if not grid:
                    raise ChartError(
                        "Layout grid setting must be set "
                        "if layout type is 'grid'")

                if not grid.get('location'):
                    raise ChartError(
                        "Layout grid location must be set "
                        "if layout type is 'grid'")

                if len(grid['location']) != 2:
                    raise ChartError("Layout grid location length must be 2")

    def validate(self):
        """Validate all config attributes."""
        validation_methods = get_validation_methods(LayoutConfig)

        for method in validation_methods:
            getattr(self, method)()


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


def build_secondary_axis(axis, on='x'):
    """Build twin secondary axis."""
    methods = {
        'x': 'twinx',
        'y': 'twiny',
    }
    method = getattr(axis, methods[on])
    return method()


def customize_axis(axis, params):
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


def build_series(axis, params):
    """Build series plot on the axis based on series data."""

    config = SeriesConfig(**params)
    plot_data = resolve_data(config)

    gca = build_secondary_axis(
        axis, on=config.secondary) if config.secondary else axis
    plot = getattr(gca, SUPPORTED_TYPES[config.type])
    partial(plot, *plot_data, **config.plot_params)()

    set_axis_label(gca, 'x', config.labels.get('x'))
    set_axis_label(gca, 'y', config.labels.get('y'))

    set_axis_locator(gca, on='x', which='major',
                     params=config.locator.get('major'))
    set_axis_locator(gca, on='y', which='minor',
                     params=config.locator.get('minor'))

    set_axis_formatter(gca, on='x', which='major',
                       params=config.formatter.get('major'))
    set_axis_formatter(gca, on='y', which='minor',
                       params=config.formatter.get('minor'))

    gca.set_title(config.title)
    set_axis_legend(gca, config.legend)

    customize_axis(axis, params)

    return gca


class Chart(object):
    """A chart object."""

    def __init__(self, config):
        self.config = config.copy()
        self.title = config.get('title')
        self.theme = config.get('theme', 'classic')
        self.legend = config.get('legend', {})

        self.starttime = utils.to_pydatetime(config.get('starttime'))
        self.endtime = utils.to_pydatetime(config.get('endtime'))

        config_layout = config.get('layout', {})
        self.layout = LayoutConfig(**config_layout)

        self.figure_options = config.get('figure_options', {})
        self.save_options = config.get('save_options', {})
        self.extensions = config.get('extensions', {})

        self.figure = None
        self.axes = []
        self.rendered_axes = []

        self._validate()

    def _validate(self):
        self.layout.validate()

        for layout in self.layout.data:
            layout_series = layout.get('series')
            if layout_series:
                for params in layout_series:
                    config = SeriesConfig(**params)
                    config.validate()

    @cached_property
    def num_subplots(self):
        """Get number of subplots."""
        return len(self.layout.data)

    def _build_series_legend(self, axis, handles, labels, params=None):
        options = params or {}

        if options.pop('show', False):
            axis.legend(handles, labels, **options)

    def _build_layout(self, axis, layout):
        if not layout.get('series'):
            return None

        subplot_axes = []
        subplot_handles = []
        subplot_labels = []

        for series_data in layout['series']:
            gca = build_series(axis, series_data)
            subplot_axes.append(gca)

            handle, label = gca.get_legend_handles_labels()
            subplot_handles += handle
            subplot_labels += label

        self._build_series_legend(
            gca, subplot_handles, subplot_labels, layout.get('legend', {}))

        return subplot_axes

    def _build_figure(self):
        self.figure = plt.figure(**self.figure_options)

    def _build_axes_rank(self):
        share = []
        for index in range(self.num_subplots):
            if self.layout.type == 'grid':
                options = self.layout.data[index]['grid'].get('options', {})
            else:
                options = self.layout.data[index].get('options', {})
            sharex = options.get('sharex', -1)
            share.append(sharex)
            sharey = options.get('sharey', -1)
            share.append(sharey)

        results = [(share.count(index), index)
                   for index in range(self.num_subplots)]

        return sorted(results, reverse=True)

    def _build_axes(self):
        keys = ['sharex', 'sharey']

        if self.layout.type == 'grid':
            layout_size = self.layout.size

            rank = self._build_axes_rank()
            for _, index in rank:
                grid = self.layout.data[index]['grid']
                location = grid['location']
                options = grid.get('options', {})

                for key in keys:
                    share_index = options.get(key)
                    if share_index:
                        options.update({key: self.axes[share_index]})
                self.axes[index] = plt.subplot2grid(
                    layout_size, location, **options)
        else:
            num_columns = 1
            options = self.layout.options

            self.figure, self.axes = plt.subplots(
                self.num_subplots, num_columns, **options)

    def _build_extension_series(self, axis):
        handles = []
        labels = []
        plot = copy.deepcopy(self.extensions.get('plot', {}))

        for key, value in plot.items():
            if key in extensions.SUPPORTED_EXTENSIONS:
                if value.pop('show', False):
                    method = getattr(
                        extensions,
                        extensions.SUPPORTED_EXTENSIONS[key]['resolver'])

                    labels.append(value.pop(
                        'label',
                        extensions.SUPPORTED_EXTENSIONS[key]['label']))

                    handle = method(axis, self.starttime,
                                    self.endtime, **value)
                    handles.append(handle)

        return handles, labels

    def _build_extension_plot(self, axis):
        handles, labels = self._build_extension_series(axis)
        legend = self.extensions.pop('legend', {})

        if legend:
            show = legend.pop('show', False)
            if show:
                self.figure.legend(handles, labels, **legend)

    def render(self):
        """Render chart object."""

        apply_theme(self.theme)

        self.axes = [None] * self.num_subplots
        self.rendered_axes = []

        self._build_figure()
        self._build_axes()

        if not self.num_subplots:
            return

        if self.num_subplots == 1:
            self.axes = [self.axes]

        for axis, layout in zip(self.axes, self.layout.data):
            subplot_axes = self._build_layout(axis, layout)
            self.rendered_axes.append(subplot_axes)
            self._build_extension_plot(axis)

    def save(self, filename):
        """Export chart object to file."""

        plt.title(self.title)
        plt.tight_layout(**self.config.get('tight_layout', {}))
        plt.savefig(filename, **self.save_options)

    def clear(self):
        """Clear all chart axes and figures."""

        if self.figure:
            plt.close(self.figure)
