import re
from cached_property import cached_property

import matplotlib.pyplot as plt
import matplotlib.ticker
import matplotlib.gridspec as gridspec

from pandas.plotting import register_matplotlib_converters

from .client import fetch_as_dataframe
from .utils import resolve_timestamp
from .exceptions import ChartError
from .processing import dataframe_or_empty


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

    required_parameters = ['name', 'fields']

    def __init__(self, **kwargs):
        self.type = kwargs.get('type', 'line')
        if self.type == 'line':
            self.type = 'plot'

        self.name = kwargs.get('name')
        self.query_params = kwargs.get('query_params', {})
        self.fields = kwargs.get('fields', [])
        self.plot_params = kwargs.get('plot_params', {})
        self.labels = kwargs.get('labels', {})
        self.locator = kwargs.get('locator', {})
        self.formatter = kwargs.get('formatter', {})
        self.aggregation = kwargs.get('aggregation', [])
        self.secondary = kwargs.get('secondary', False)
        self.legend = kwargs.get('legend', {})
        self.title = kwargs.get('title')

        self._check_required_parameters(kwargs)

    def _check_required_parameters(self, kwargs):
        for param in self.required_parameters:
            if param not in kwargs:
                raise ChartError('Parameter {} is required'.format(param))

    def validate_name(self):
        """Validate name attribute."""
        if self.name not in SUPPORTED_NAMES:
            raise ChartError('Unknown parameter name {}'.format(self.name))

    def validate_fields(self):
        """Validate fields attribute."""
        if not self.fields:
            raise ChartError('Series fields must be set')

    def validate(self):
        """Validate all attributes."""
        validation_methods = get_validation_methods(SeriesConfig)

        for method in validation_methods:
            getattr(self, method)()


class LayoutConfig(object):

    def __init__(self, **kwargs):
        self.type = kwargs.get('type', 'default')
        self.size = kwargs.get('size', [])
        self.data = kwargs.get('data', [])
        self.options = kwargs.get('options', {})

    def validate_size(self):
        if self.type == 'grid':
            if not self.size:
                raise ChartError(
                    "Layout size must be set "
                    "if layout type is 'grid'")

            if len(self.size) != 2:
                raise ChartError('Layout size length must be 2')

    def validate_data(self):
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


def normalize_series(series):
    supported_types = {
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


def build_series(axis, params):
    """Build series plot on the axis based on series data."""

    config = SeriesConfig(**params)
    data = fetch_as_dataframe(config.name, config.query_params)

    xdata = dataframe_or_empty(data, config.fields[0])
    xdata = resolve_timestamp(xdata)
    ydata = dataframe_or_empty(data, config.fields[1])

    gca = axis.twinx() if config.secondary else axis
    plot = getattr(gca, config.type)
    series = plot(xdata, ydata, **config.plot_params)

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
    gca.xaxis_date()

    return series, gca


class Chart(object):
    """A chart object."""

    def __init__(self, **config):
        # self.starttime = config.get('starttime')
        # self.endtime = config.get('endtime')

        self.title = config.get('title')
        self.theme = config.get('theme', 'classic')
        self.legend = config.get('legend', {})

        # self.dpi = config.get('dpi', 72)
        # self.width = config.get('width', 640)
        # self.height = config.get('height', 480)
        # self.subplot_height = config.get('subplot_height', 72)

        config_layout = config.get('layout', {})
        self.layout = LayoutConfig(**config_layout)

        self.figure_options = config.get('figure_options', {})
        self.save_options = config.get('save_options', {})

        self.figure = None
        self.axes = []

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

    def _build_layout(self, axis, layout):
        if not layout.get('series'):
            return None, None

        subplot_series = []
        subplot_axes = []

        for series_data in layout['series']:
            series, gca = build_series(axis, series_data)

            subplot_series.append(series)
            subplot_axes.append(gca)

        return subplot_series, subplot_axes

    def _build_figure(self):
        self.figure = plt.figure()

    def _build_axes(self):
        if self.layout.type == 'grid':
            layout_size = self.layout.size

            for layout in self.layout.data:
                grid = layout['grid']
                location = grid['location']
                options = grid.get('options', {})
                self.axes.append(plt.subplot2grid(
                    layout_size, location, fig=self.figure, **options))
        else:
            num_columns, column_index = 1, 0
            layout_size = [self.num_subplots, num_columns]
            options = self.layout.options

            for row_index in range(self.num_subplots):
                self.axes.append(plt.subplot2grid(
                    layout_size, [row_index, column_index], fig=self.figure,
                    **options))

    def render(self):
        """Render chart object."""

        apply_theme(self.theme)
        self._build_figure()
        self._build_axes()

        if not self.axes:
            return

        for axis, layout in zip(self.axes, self.layout.data):
            self._build_layout(axis, layout)

        self.figure.autofmt_xdate()

    def save(self, filename):
        """Export chart object to file."""

        plt.title(self.title)
        plt.tight_layout()
        plt.savefig(filename, **self.save_options)
