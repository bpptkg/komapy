import re
from cached_property import cached_property

import matplotlib.pyplot as plt
import matplotlib.ticker

from pandas.plotting import register_matplotlib_converters

from .client import fetch_as_dataframe
from .utils import resolve_timestamp
from .exceptions import ChartError
from .processing import dataframe_or_empty


register_matplotlib_converters()

re_validate_template = re.compile('validate_(?P<name>\w+)')

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


class SeriesConfig(object):
    """A series config object."""

    required_parameters = ['type', 'name', 'fields']

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

        self._check_required_parameters(kwargs)

    def _check_required_parameters(self, kwargs):
        for param in self.required_parameters:
            if param not in kwargs:
                raise ChartError('Parameter {} is required'.format(param))

    def validate_name(self):
        """Validate name attribute."""
        if self.name not in self.required_parameters:
            raise ChartError('Unknown parameter name {}'.format(self.name))

    def validate_fields(self):
        """Validate fields attribute."""
        if len(self.fields) < 2:
            raise ChartError('Not enough series fields')

    def validate(self):
        """Validate all attributes."""
        validation_methods = []
        for item in self.__dict__:
            matched = re_validate_template.match(item)
            if matched:
                validation_methods.append(matched.groupdict().get('name'))

        for method in validation_methods:
            method()


def set_axis_locator(axis, which='major', params=None):
    """Set axis locator."""
    config = params or {}
    methods = {
        'major': 'set_major_locator',
        'minor': 'set_minor_locator',
    }

    locator = getattr(matplotlib.ticker, config.get('name', ''), None)
    if locator:
        getattr(axis.yaxis, methods[which])(
            locator(**config.get('params', {})))


def set_axis_formatter(axis, which='major', params=None):
    """Set axis formatter."""
    config = params or {}
    methods = {
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
        getattr(axis.yaxis, methods[which])(formatter(config.get('format')))


def build_series(axis, params):
    """Build series plot on the axis based on series data."""

    config = SeriesConfig(**params)
    config.validate()

    data = fetch_as_dataframe(config.name, config.query_params)

    xdata = dataframe_or_empty(data, config.fields[0])
    xdata = resolve_timestamp(xdata)
    ydata = dataframe_or_empty(data, config.fields[1])

    gca = axis.twinx() if config.secondary else axis
    plot = getattr(gca, config.type)
    series = plot(xdata, ydata, **config.plot_params)

    ylabel = config.labels.get('y', {})
    gca.set_ylabel(ylabel.get('text'), **ylabel.get('style', {}))

    set_axis_locator(gca, which='major', params=config.locator.get('major'))
    set_axis_locator(gca, which='minor', params=config.locator.get('minor'))

    set_axis_formatter(gca, which='major',
                       params=config.formatter.get('major'))
    set_axis_formatter(gca, which='minor',
                       params=config.formatter.get('minor'))

    return series, (axis, gca)


class Chart(object):
    """A chart object."""

    def __init__(self, **config):
        self.starttime = config.get('starttime')
        self.endtime = config.get('endtime')

        self.title = config.get('title')
        self.theme = config.get('theme', 'classic')
        self.legend = config.get('legend', True)

        self.dpi = config.get('dpi', 72)
        self.width = config.get('width', 640)
        self.height = config.get('height', 480)
        self.subplot_height = config.get('subplot_height', 72)

        self.layout = config.get('layout', [])

        self.figure = None
        self.axes = []
        self.series = []

    @cached_property
    def num_subplots(self):
        """Get number of subplots."""
        return len(self.layout)

    @cached_property
    def figure_size_in_inches(self):
        """Get chart figure size."""
        if self.num_subplots > 1:
            return (
                (self.width / self.dpi),
                (self.subplot_height * self.num_subplots) / self.dpi
            )
        return (self.width / self.dpi, self.height / self.dpi)

    @cached_property
    def figure_size_in_pixel(self):
        """Get chart figure size in pixel."""
        if self.num_subplots > 1:
            return (self.width, self.subplot_height * self.num_subplots)
        return (self.width, self.height)

    def _build_layout(self, axis, layout):
        if not layout.get('series'):
            return

        for series_data in layout.get('series'):
            series, axis_pair = build_series(axis, series_data)
            
            self.series.append(series)
            self.axes.append(axis_pair)

    def render(self):
        """Render chart object."""

        apply_theme(self.theme)

        ncols = 1
        nrows = self.num_subplots
        self.figure, self.axes = plt.subplots(
            nrows=nrows,
            ncols=ncols,
            sharex=True,
            figsize=self.figure_size_in_inches
        )

        if len(self.axes) == 1:
            self.axes = list(self.axes)

        if not nrows:
            return

        for axis, layout in zip(self.axes, self.layout):
            self._build_layout(axis, layout)

    def save(self, filename):
        """Export chart object to file."""

        self.figure.tight_layout()
        plt.title(self.title)
        plt.savefig(filename)
