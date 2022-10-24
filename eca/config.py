#!/usr/bin/env python3

from datetime import timedelta
from eca.sources import TextEvents
import eca.dateparser
import os
from eca.normalizer import Normalizer
from typing import Iterator
import yaml

class Config:
    global_defaults = {
        "range": "1s",
        "percentile": 90,
        "accuracy": 90,
    }

    source_defaults = {
        'master': False,
        'date-format': 'auto',
        'type': 'text-events',
        'categories': ['main'],
    }

    def __init__(self, filename):
        self._dir = os.path.dirname(filename)
        self._event_sources = list()
        with open(filename, "r") as stream:
            self._config = yaml.safe_load(stream)

        # Set global defaults
        for k, v in Config.global_defaults.items():
            self._config.setdefault(k, v)

        # Set per source defaults
        for e in self._config['sources']:
            for k, v in Config.source_defaults.items():
                e.setdefault(k, v)

            filename = e['filename'] if os.path.isabs(e['filename']) else os.path.join(self._dir, e['filename'])

            date_parser = eca.dateparser.create_parser_from_str(e['date-format'])

            if e['type'] == 'text-events':
                es = TextEvents(filename=filename, date_parser=date_parser, master=e['master'])
            else:
                raise RuntimeError(f"unknown event type: {e['type']}")

            for n in e.get('normalizers', []):
                es.add_normalizer(Normalizer.create_from_str(n))

            self._event_sources.append(es)

    def event_sources(self, master: bool = None) -> Iterator[eca.sources.TextEvents]:
        """Return list of even sources."""
        for es in self._event_sources:
            if master is None or master == es.is_master():
                yield es

    @property
    def range(self) -> timedelta:
        if self._config['range'].endswith('s'):
            return timedelta(seconds=float(self._config['range'][:-1]))
        else:
            raise RuntimeError(f"Unknown time format for range: {self._config['range']}")

    @property
    def percentile(self) -> int:
        return self._config['percentile']

    @property
    def accuracy(self) -> int:
        return self._config['accuracy']


if __name__ == "__main__":
    c = Config("tests/config/conf1.yaml")
    print(c.sources)
