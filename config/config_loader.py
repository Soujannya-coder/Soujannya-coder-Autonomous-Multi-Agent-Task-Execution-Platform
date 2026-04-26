# config/config_loader.py

import yaml
import os

class Config:
    def __init__(self, path: str = None):
        if path is None:
            # default path relative to project root
            path = os.path.join("config", "config.yaml")

        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found at {path}")

        with open(path, "r") as f:
            self._data = yaml.safe_load(f)

    def get(self, *keys, default=None):
        data = self._data
        for key in keys:
            if not isinstance(data, dict) or key not in data:
                return default
            data = data[key]
        return data

    @property
    def raw(self):
        return self._data