"""
KomaPy app settings.
"""

from .constants import TIME_ZONE


class AppSettings:
    """
    A settings object. It defines access to the BMA API using API key or
    access token and other setting parameters.
    """

    api_key = ''
    access_token = ''
    protocol = ''
    time_zone = TIME_ZONE
    host = ''
    bma_api_class = None


app_settings = AppSettings()
