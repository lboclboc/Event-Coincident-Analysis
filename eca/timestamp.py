#!/usr/bin/env python3

from datetime import datetime, timedelta
from typing import List

class TimestampDB:
    """Database of timestamps."""
    def __init__(self, range: timedelta = timedelta(seconds=2)):
        self._range = range
        self._timestamps: List[datetime] = list()
        self._prepared: bool = True
        self._youngest: datetime = None
        self._oldest: datetime = None

    def append(self, timestamp: datetime) -> None:
        self._timestamps.append(timestamp)
        self._prepared = False

    def _prepare(self):
        """
        Prepare db for being used for comparising.

        Its necessary to have dates sorted and also to know which is the youngest and oldest timestamps.
        """
        self._timestamps = sorted(self._timestamps)
        for ts in self._timestamps:
            if self._youngest is None or ts > self._youngest:
                self._youngest = ts
            if self._oldest is None or ts < self._oldest:
                self._oldest = ts

        self._prepared = True

    def __iter__(self):
        if not self._prepared:
            self._prepare()

        return (t for t in self._timestamps)

    def __len__(self) -> int:
        return len(self._timestamps)

    def is_applicable(self, timestamp):
        """Return true if timestamp is applicable for comparing."""
        if not self._prepared:
            self._prepare()
        return timestamp > (self._oldest - self._range) and timestamp < (self._youngest + self._range)

    def in_range(self, timestamp: datetime) -> bool:
        """Returns True if timestamp is within the range of timestamps for this database."""
        for ts in self:
            if timestamp + self._range > ts and timestamp < ts + self._range:
                return True
        else:
            return False
