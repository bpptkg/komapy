"""
KomaPy Chart.

KomaPy chart design philosophy is only use config to create customizable chart.
It wraps matplotlib axes object and provides BMA data fetching mechanism that
allow user to create customizable chart with ease and simplicity.

Example:

from komapy import Chart

chart = Chart({
    'title': 'RB2',
    'theme': 'seaborn',
    'layout': {
        'data': [
            {
                'series': [
                    {
                        'name': 'edm',
                        'query_params': {
                            'benchmark': 'BAB0',
                            'reflector': 'RB2',
                            'start_at': '2019-04-01',
                            'end_at': '2019-08-01',
                            'ci': True
                        },
                        'fields': ['timestamp', 'slope_distance'],
                        'xaxis_date': True
                    }
                ]
            }
        ]
    }
})

chart.render()
chart.save('RB2.png')
"""

import copy
from cached_property import cached_property
from collections import Callable

import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

from . import extensions
from . import utils
from .exceptions import ChartError
from .layout import Layout
from .settings import app_settings
from .series import Series, build_series

register_matplotlib_converters()

__all__ = [
    'Chart',
]


def apply_theme(name):
    """Apply matplotlib plot theme."""
    if name in plt.style.available:
        plt.style.use(name)


class Chart(object):
    """A chart object."""

    def __init__(self, config):
        self.config = copy.deepcopy(config)

        self.title = config.get('title')
        self.theme = config.get('theme', 'classic')
        self.legend = config.get('legend', {})
        self.timezone = config.get('timezone', app_settings.time_zone)

        config_layout = config.get('layout', {})
        self.layout = Layout(**config_layout)

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
            if isinstance(layout_series, list):
                for params in layout_series:
                    config = Series(**params)
                    config.validate()
            elif isinstance(layout_series, dict):
                params = layout_series
                config = Series(**params)
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
        subplot_axes = []
        if not layout.get('series'):
            return subplot_axes

        subplot_handles = []
        subplot_labels = []
        if isinstance(layout['series'], list):
            for series_data in layout['series']:
                gca = build_series(axis, series_data)
                subplot_axes.append(gca)

                handle, label = gca.get_legend_handles_labels()
                subplot_handles += handle
                subplot_labels += label
        elif isinstance(layout['series'], dict):
            gca = build_series(axis, layout['series'])
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

    def _build_extension_series(self, axis, starttime, endtime):
        if not starttime:
            raise ChartError(
                'Parameter starttime is required to build extension series')
        if not endtime:
            raise ChartError(
                'Parameter endtime is required to build extension series')

        handles = []
        labels = []
        plot = copy.deepcopy(self.extensions.get('plot', []))

        for item in plot:
            name = item.pop('name', None)
            if name is None:
                raise ChartError(
                    'Parameter name is required to build extension series')

            if isinstance(name, Callable):
                method = name
                labels.append(item.pop('label', ''))
                handle = method(axis, starttime, endtime, **item)
            else:
                if name not in extensions.supported_extensions:
                    continue
                resolver = extensions.supported_extensions[name]['resolver']
                if isinstance(resolver, Callable):
                    method = resolver
                elif isinstance(resolver, str):
                    method = getattr(
                        extensions,
                        extensions.supported_extensions[name]['resolver'])

                labels.append(item.pop(
                    'label',
                    extensions.supported_extensions[name].get('label', '')))
                handle = method(axis, starttime, endtime, **item)

                if handle:
                    handles.append(handle)
                else:
                    labels.pop()

        return handles, labels

    def _build_extension_plot(self, axis):
        if self.extensions:
            starttime = utils.to_pydatetime(
                self.extensions['starttime'],
                timezone=self.timezone
            ) if self.extensions.get('starttime') else None

            endtime = utils.to_pydatetime(
                self.extensions['endtime'],
                timezone=self.timezone
            ) if self.extensions.get('endtime') else None

            handles, labels = self._build_extension_series(
                axis, starttime, endtime)
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

        if self.num_subplots > 1:
            self.figure.suptitle(self.title)
        else:
            plt.title(self.title)
        plt.tight_layout(**self.config.get('tight_layout', {}))
        plt.savefig(filename, **self.save_options)

    def clear(self):
        """Clear all chart axes and figures."""

        if self.figure:
            plt.close(self.figure)
