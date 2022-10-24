#!/usr/bin/env python3
from collections import defaultdict
import eca.config
from eca.timestamp import TimestampDB
import sys

def main():
    if len(sys.argv) != 2:
        raise RuntimeError("Usage: eca <yaml-config-file>")
    config = eca.config.Config(sys.argv[1])

    # Collect all timestamps for incidents.
    timestamps: TimestampDB = TimestampDB(range=config.range)
    for s in config.event_sources(master=True):
        for ts, line in s.get_events():
            timestamps.append(ts)

    # Collect all texts and if they are applicable order into either within or outside
    # event timestamps.
    texts_within = defaultdict(int)
    texts_outside = defaultdict(int)
    for es in config.event_sources(master=False):
        for ts, line in es.get_events():
            line = es.normalize(line)
            if timestamps.is_applicable(ts):
                if timestamps.in_range(ts):
                    texts_within[line] += 1
                    print(f"inside:  {ts} - {line}")
                else:
                    texts_outside[line] += 1
                    print(f"outside: {ts} - {line}")

    # Find texts that only occur close to incident events but not otherwise.
    for txt in texts_within:
        if txt not in texts_outside:
            print(f"Text only occuring during incident event: {txt}")

    print(f"total {len(timestamps)} incidents, {len(texts_within)} unique texts found inside event range, {len(texts_outside)} outside")


if __name__ == "__main__":
    main()
