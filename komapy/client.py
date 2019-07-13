import json
import bmaclient

from six.moves.urllib.request import urlopen
from six.moves.urllib.parse import urlencode

from . import processing
from . import exceptions


def fetch_bma_as_json(name, params=None):
    """Make a request to the BMA API and return data as json."""
    api = bmaclient.MonitoringAPI()
    method = api.get_fetch_method(name)
    if not method:
        raise exceptions.ChartError('Unknown parameter name {}'.format(name))
    query_params = params or {}
    return method(**query_params)


def fetch_bma_as_dataframe(name, params=None):
    """Make a request to the BMA API and return data as Pandas DataFrame."""
    response = fetch_bma_as_json(name, params)
    return processing.dataframe_from_dictionary(response)


def fetch_url_as_json(url, params=None):
    """Make a request to the URL and return as json."""
    full_query_params = '?{}'.format(urlencode(params)) if params else ''
    full_url_with_params = '{url}{query_params}'.format(
        url=url,
        query_params=full_query_params
    )

    with urlopen(full_url_with_params) as content:
        data = json.loads(content.read().decode('utf-8'))

    return data


def fetch_url_as_dataframe(url, params=None):
    """Make a request to the URL and return data as Pandas DataFrame."""
    response = fetch_url_as_json(url, params)
    return processing.dataframe_from_dictionary(response)
