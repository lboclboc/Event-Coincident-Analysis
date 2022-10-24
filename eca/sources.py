#!/usr/bin/env python3
from datetime import datetime
from typing import List, Tuple, Iterator
from eca.normalizer import Normalizer
from eca.dateparser import DateParser


class TextEvents:
    """Source of text based events."""
    def __init__(self, filename, date_parser, master):
        self._filename: str = filename
        self._date_parser: DateParser = date_parser
        self._master: bool = master
        self._normalizers: List[Normalizer] = []

    def add_normalizer(self, normalizer: Normalizer) -> None:
        self._normalizers.append(normalizer)

    def normalize(self, line: str) -> str:
        for n in self._normalizers:
            line = n.normalize(line)
        return line

    def is_master(self) -> bool:
        return self._master

    def get_events(self) -> Iterator[Tuple[datetime, str]]:
        with open(self._filename) as fin:
            for line in fin.readlines():
                line = line.strip()
                res = self._date_parser.process(line)
                if res[0]:
                    yield res
