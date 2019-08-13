"""
KomaPy app settings.
"""

from .constants import TIME_ZONE


class AppSettings:
    """
    A settings object. It defines access to the BMA API using API Key or
    access token.
    """

    api_key = None
    access_token = None
    time_zone = TIME_ZONE


app_settings = AppSettings()
