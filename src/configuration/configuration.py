import json
import os


class Configuration:
    def __init__(self, configuration_file_path='/data/options.json'):
        with open(configuration_file_path) as options_file:
            self._settings = json.load(options_file)

    def __getitem__(self, key):
        return self._settings[key]

    def get(self, key, default=None):
        return self._settings.get(key, default)
