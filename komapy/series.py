"""
KomaPy chart series.
"""

from collections import Callable, OrderedDict
from functools import partial

from . import client, processing, transforms, utils
from .constants import SUPPORTED_NAMES, SUPPORTED_TYPES
from .exceptions import ChartError
from .utils import get_validation_methods

addon_registers = {

}


def register_addon(name, resolver):
    """
    Register add-on function.

    :param name: Name of addon register.
    :type name: str
    :param resolver: Addon callable resolver function.
    :type resolver: :class:`collections.Callable`
    """
    if not isinstance(resolver, Callable):
        raise ChartError('Add-on resolver must be callable')

    if name in addon_registers:
        raise ChartError('Add-on name already exists')

    addon_registers[name] = resolver


class Series(object):
    """
    A series object.

    A series object in KomaPy holds information about series data, including
    plot type, plot data, data query parameters, axis locator, axis formatter,
    and many more. Here it is an example on how to create series instance:

    .. code-block:: python

        from komapy.series import Series

        series = Series(
            name='edm',
            query_params={
                'benchmark: 'BAB0',
                'reflector': 'RB2',
                'start_at': '2019-04-01',
                'end_at: '2019-08-01',
                'ci': True
            },
            plot_params={
                'color': 'k',
                'marker': 'o',
                'markersize': 6,
                'zorder': 2,
                'linewidth': 1,
                'label': 'RB2'
            },
            fields=['timestamp', 'slope_distance'],
            xaxis_date=True
        )

        series.validate()
        data = series.resolve_data()

    Below is the list of available series property. The only required property
    to be set is ``fields`` property.


    ``addons``

    type: list

    default: []

    Series plot addons. Each addons entry contains a dictionary of addons
    configuration. The only required key is ``name``. Other keys left as
    optional parameter and will be passed to particular addons resolver.

    Example:

    .. code-block:: python

        series = Series(
            addons=[
                {
                    name: 'addon',
                }
            ]
        )


    ``aggregations``

    type: list

    default: []

    Series data aggregations. Data aggregation allows to manipulate plot data
    for specific field without affecting another field before it get rendered
    into the chart object. Each aggregations entry contains a dictionary of
    aggregation configuration. Required key are ``func`` which is a name of
    aggregation function and ``field`` which is name of data field the resolver
    should target. Other key is ``params`` which is a dictionary argument that
    will be passed to the aggregation resolver function.

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


    ``csv_params``

    type: dict

    default: {}

    CSV parameters to be passed to the CSV resolver. Default CSV resolver is
    ``pandas.read_csv``. So, all parameters will be passed as keyword arguments
    to the pandas read_csv keyword arguments.


    ``csv``

    type: str

    default: None

    Path to the CSV file or CSV URL.

    Example:

    .. code-block:: python

        series = Series(csv='http://api.example.com/data.csv')


    ``fields``

    type: list, function

    default: []

    Data fields to plot. If using CSV, JSON URL, or BMA API name, fields can be
    a list of column name or JSON field name you want to plot. If you want to
    plot timestamp vs energy, you can write the fields like this:
    ``['timestamp', 'energy']``.

    Example:

    .. code-block:: python

        series = Series(name='energy', fields=['timestamp', 'energy'])


    ``formatter``

    type: dict

    default: {}

    Axis formatter configuration. The parameters will be passed to the
    Matplotlib axis formatter class.

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


    ``grid``

    type: dict

    default: {}

    Grid parameters used in grid layout.

    TODO: Add example.


    ``labels``

    type: dict

    default: {}

    Axis label configuration. The parameters will be passed to the Matplotlib
    axis ``set_xlabel`` or ``set_ylabel`` methods.

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

    
    ``legend``

    type: dict

    default: {}

    Axis legend configuration. The parameters will be passed to the Matplotlib
    axis legend method. The only required parameter is ``show`` which is a
    boolean value indicating the legend should be drawn or not.

    Example:

    .. code-block:: python

        series = Series(
            legend={
                'show': True,
                'loc: 'upper left'
            }
        )

    
    ``locator``

    type: dict

    default: {}

    Axis locator configuration. The parameters will be passed to the Matplotlib
    axis locator class.

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


    ``name``

    type: str

    default: None

    BMA API name like ``doas``, ``edm``, ``tiltmeter``, ``seismicity``, etc.

    Example:

    .. code-block:: python

        series = Series(name='seismicity')

    
    ``plot_params``

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

    
    ``query_params``

    type: dict

    default: {}

    URL query parameters. The parameters will be used as field query filtering
    for BMA API name or URL query parameters.

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

    
    ``secondary``

    type: str

    default: None

    Name of axis to build secondary axis. Accepted name are ``x`` for x axis,
    and ``y`` for y axis.

    Example:

    .. code-block:: python

        series = Series(secondary='x')

    
    ``title``

    Series title name.

    Example:

    .. code-block:: python

        series = Series(title='RB2')


    ``transforms``

    type: list

    default: []

    Series data transformations. Data transformation allows changes to the plot
    data before it rendered into the chart object. Some example is to transfrom
    EDM data to apply slope distance correction after data had been resolved.

    Each entry contains a function of data transformation, or a string if the
    function has been registered to the KomaPy data transformation registers.

    Example:

    .. code-block:: python

        series = Series(
            transforms=[
                'slope_correction'
            ]
        )

    
    ``type``

    type: str

    default: line

    Name of series plot type. Default value is line plot. Accepted values
    include bar, errorbar, scatter, etc.

    Example:

    .. code-block:: python

        series = Series(type='bar')

    
    ``url``

    A URL that returns JSON data. KomaPy will fetch the data from the URL
    and use it as data source.

    Example:

    .. code-block:: python

        series = Series(
            url='http://cendana15.com/api/analytics/edm?start_at=2019-04-01&end_at=2019-08-01'
        )

    
    ``xaxis_date``

    type: boolean

    default: False

    Tells if the x axis should be using datetime format or not. KomaPy will
    convert the value to the datetime value.

    Example:

    .. code-block:: python

        series = Series(xaxis_date=True)


    ``yaxis_date``

    type: boolean

    default: False

    Tells if the y axis should be using datetime format or not. KomaPy will
    convert the value to the datetime value.

    Example:

    .. code-block:: python

        series = Series(yaxis_date=True)

    """

    required_parameters = ['fields']
    available_parameters = {
        'addons': [],
        'aggregations': [],
        'csv_params': {},
        'csv': None,
        'fields': [],
        'formatter': {},
        'grid': {},
        'labels': {},
        'legend': {},
        'locator': {},
        'name': None,
        'plot_params': {},
        'query_params': {},
        'secondary': None,
        'title': None,
        'transforms': [],
        'type': 'line',
        'url': None,
        'xaxis_date': False,
        'yaxis_date': False,
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

    def resolve_data(self):
        """
        Resolve plot data.

        Plot data is resolved in the following order, CSV, JSON URL, and BMA API
        name. Each of sources has certain resolver. If none of the sources found
        in the chart series, data source is treated as plain object.

        :return: A list of resolved plot data whose type of
                 :class:`pandas.DataFrame` if using CSV, JSON URL, or BMA API
                 name. Otherwise, it returns native object.
        :rtype: list of :class:`pandas.DataFrame` or native object
        """
        sources = OrderedDict([
            ('csv', {
                'resolver': processing.read_csv,
                'options': 'csv_params'
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
            source = getattr(self, name, None)
            if source:
                resolve = sources[name]['resolver']
                options = getattr(self, sources[name]['options'], {})
                break
        
        if source:
            resource = resolve(source, options)
            func = partial(processing.dataframe_or_empty, resource)
            iterator = map(func, self.fields)
        else:
            iterator = self.fields

        plot_data = []
        for i, field in enumerate(iterator):
            if i == 0 and self.xaxis_date:
                plot_data.append(utils.resolve_timestamp(field))
            elif i == 1 and self.yaxis_date:
                plot_data.append(utils.resolve_timestamp(field))
            else:
                plot_data.append(field)

        if self.aggregations:
            for item in self.aggregations:
                func = item.get('func')
                if func is None:
                    raise ChartError(
                        'Function name or callable must be set '
                        'if using data aggregations')

                agg_field = item.get('field')
                if agg_field is None:
                    raise ChartError('Field name must be set '
                                    'if using data aggregations')
                if source:
                    index = self.fields.index(agg_field)
                else:
                    index = agg_field

                params = item.get('params', {})

                if isinstance(func, str):
                    if func not in processing.supported_aggregations:
                        continue

                    resolver = processing.supported_aggregations[func]
                    if isinstance(resolver, str):
                        callback = getattr(processing, resolver)
                    elif isinstance(resolver, Callable):
                        callback = resolver
                    plot_data[index] = callback(plot_data[index], params)

                elif isinstance(func, Callable):
                    plot_data[index] = callback(plot_data[index], params)

        if self.transforms:
            for item in self.transforms:
                if isinstance(item, str):
                    if item not in transforms.transform_registers:
                        continue

                    resolver = transforms.transform_registers[item]
                    if isinstance(resolver, str):
                        callback = getattr(transforms, resolver)
                    elif isinstance(resolver, Callable):
                        callback = resolver
                    plot_data = callback(plot_data, self)

                elif isinstance(item, Callable):
                    plot_data = callback(plot_data, self)

        return plot_data
