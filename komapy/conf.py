import json

from .settings import AppSettings, app_settings

_cached_attrs = {}


class Settings:
    """
    A proxy to get or set app settings.
    """

    def __getattr__(self, attr):
        if attr in _cached_attrs:
            return _cached_attrs[attr]
        return getattr(app_settings, attr, None)

    def __setattr__(self, attr, value):
        if hasattr(app_settings, attr):
            setattr(app_settings, attr, value)
        _cached_attrs[attr] = value

    def from_dict(self, settings):
        """
        Set settings from dictionary object.
        """
        for attr, value in settings.items():
            setattr(self, attr, value)

    def from_json(self, settings):
        """
        Set settings from JSON object.
        """
        dict_settings = json.loads(settings)
        self.from_dict(dict_settings)

    def from_json_file(self, path):
        """
        Set settings from JSON file.
        """
        with open(path) as fp:
            dict_settings = json.load(fp)
        self.from_dict(dict_settings)

    def reset(self):
        """
        Reset settings to default.
        """
        _cached_attrs.clear()
        app_settings = AppSettings()

    def clear(self):
        """
        Clear cached settings.
        """
        _cached_attrs.clear()


settings = Settings()