from functools import partial

from .constants import SUPPORTED_NAMES, SUPPORTED_TYPES
from .exceptions import ChartError
from .utils import get_validation_methods
from .axis import (
    resolve_data, set_axis_formatter, set_axis_label, set_axis_legend,
    set_axis_locator, customize_axis, build_secondary_axis
)


class Series(object):
    """A series object."""

    required_parameters = ['fields']
    available_parameters = {
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
        for key, value in self.available_parameters.items():
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
        validation_methods = get_validation_methods(Series)

        for method in validation_methods:
            getattr(self, method)()


def build_series(axis, params):
    """Build series plot on the axis based on series data."""

    config = Series(**params)
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
