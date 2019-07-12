import bmaclient

from . import processing
from . import exceptions


def fetch_as_json(name, params=None):
    """Make a request to the BMA API and return data as json."""
    api = bmaclient.MonitoringAPI()
    api.host = '203.189.89.125:8080'
    method = api.get_fetch_method(name)
    if not method:
        raise exceptions.ChartError('Unknown parameter name {}'.format(name))
    query_params = params or {}
    return method(**query_params)


def fetch_as_dataframe(name, params=None):
    """Make a request to the BMA API and return data as Pandas DataFrame."""
    response = fetch_as_json(name, params)
    return processing.dataframe_from_dictionary(response)
