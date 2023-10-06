#!/usr/bin/env python3
from abc import ABC
import eca.dateparser
from datetime import datetime
import re
from typing import Protocol, List, Tuple

class DateParser(Protocol):
    def process(self, line: str) -> Tuple[datetime, str]:
        ...

class ReParser(ABC):
    def process(self, line) -> Tuple[datetime, str]:
        """Extracts timestamp from line and return (timestamp, line-without-timestamp)."""
        match = self._re.search(line)
        if match:
            if match.group('secondsdecimals'):
                microseconds = int(1000000 * float("0." + match.group('secondsdecimals')))
            else:
                microseconds = 0

            time = datetime(int(match.group('year')),
                            int(match.group('month')),
                            int(match.group('day')),
                            int(match.group('hours')),
                            int(match.group('minutes')),
                            int(match.group('seconds')),
                            microseconds)
            line = self._re.sub('', line)
            return time, line

        return None, line

class ZuluParser(ReParser):
    """Parsers zulu or UTC timestamps."""
    _re = re.compile(r'(?P<year>\d\d\d\d)-'
                     r'(?P<month>\d\d)-'
                     r'(?P<day>\d\d)T'
                     r'(?P<hours>\d\d):'
                     r'(?P<minutes>\d\d):'
                     r'(?P<seconds>\d+)'
                     r'(?:\.)?'
                     r'(?P<secondsdecimals>\d+)?Z')

class BracketFulltimeParser(ReParser):
    _re = re.compile(r'\[?(?P<year>\d\d\d\d)-'
                     r'(?P<month>\d\d)-'
                     r'(?P<day>\d\d)'
                     r'[ T]'
                     r'(?P<hours>\d\d):'
                     r'(?P<minutes>\d\d):'
                     r'(?P<seconds>\d+)'
                     r'(?:[,\.])?'
                     r'(?P<secondsdecimals>\d+)?\]?')

class AutoParser:
    parsers: List[DateParser] = [
        ZuluParser(),
        BracketFulltimeParser(),
    ]

    def __init__(self):
        ...

    def process(self, line: str):
        for p in self.parsers:
            res = p.process(line)
            if res[0]:
                return res
        else:
            return None, line


def create_parser_from_str(type: str) -> DateParser:
    if type == 'auto':
        return eca.dateparser.AutoParser()
    else:
        raise RuntimeError(f"unknown date-parser: {type}")
