#!/usr/bin/env python3
from abc import abstractmethod
from datetime import datetime, timedelta
import logging
import re
import sys
from typing import List, Protocol

logger = logging.getLogger("eca")
logger.addHandler(logging.StreamHandler(sys.stdout))

class Parser(Protocol):
    @abstractmethod
    def set_overlap(self, o: float):
        ...
    @abstractmethod        
    def __call__(self):
        ...

class ParserFactory:
    class ISOParser:
        """Finds an ISO date in the script and parses that as time."""
        def __init__(self):
            self.re = re.compile(r'(?P<year>\d\d\d\d)-'
                                 r'(?P<month>\d\d)-'
                                 r'(?P<day>\d\d)T'
                                 r'(?P<hours>\d\d):'
                                 r'(?P<minutes>\d\d):'
                                 r'(?P<seconds>\d+)'
                                 r'(?:\.)?'
                                 r'(?P<microseconds>\d+)?Z')
            self._overlap = 1.0

        def set_overlap(self, overlap):
            self._overlap = overlap

        def __call__(self, s:str):
            if not s:
                return None
            match = self.re.search(s)
            if match:
                if match.group('microseconds'):
                    microseconds = int(1000000 * float("0." + match.group('microseconds')))
                else:
                    microseconds = 0

                time = datetime(int(match.group('year')),
                                int(match.group('month')),
                                int(match.group('day')),
                                int(match.group('hours')),
                                int(match.group('minutes')),
                                int(match.group('seconds')),
                                microseconds)
                return TimeSpan(time, timedelta(seconds=self._overlap))  # FIXME: configurable time span
            return None

    @staticmethod
    def get_parser(method: str) -> Parser:
        if method == 'iso':
            return ParserFactory.ISOParser()
        else:
            raise RuntimeError(f"Unknown parser: {method}")


class TimeSpan:
    def __init__(self, t: datetime, d: timedelta):
        self.time = t
        self.duration = d

    def is_coincident(self, other) -> bool:
        s1 = self.time
        s2 = self.time + self.duration
        o1 = other.time
        o2 = other.time + other.duration

        return not ((o1 < s1 and o2 < s1) or (o1 > s2 and o2 > s2))

def compare_files(files:List[str], parsers:List[Parser]) -> None:
    line = [None] * 2
    fin = [None] * 2
    span = [None] * 2
    do_read = [False] * 2
    coincidents = 0
    misses = 0
    with open(files[0]) as fin[0], open(files[1]) as fin[1]:
        while True:
            for i in range(2):
                span[i] = parsers[i](line[i])
                if span[i] is None:
                    do_read[i] = True

            if span[0] and span[1]:
                if span[0].is_coincident(span[1]):
                    logger.info(f"conincidence at {span[0].time} <> {span[1].time}")
                    coincidents += 1
                    do_read[0] = do_read[1] = True
                else:
                    misses += 1

                if span[0].time < span[1].time:
                    do_read[0] = True
                else:
                    do_read[1] = True

            for i in range(2):
                if do_read[i]:
                    line[i] = fin[i].readline().strip()
                    do_read[i] = False

            if line[0] == '' or line[1] == '':
                break

    return (coincidents, misses)
