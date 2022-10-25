#!/usr/bin/env python3
from collections import defaultdict
import eca.config
from eca.timestamp import TimestampDB
import logging
import sys

def escape(s):
    ret = ""
    for c in s:
        if c.isprintable():
            ret += c
        elif c <= '\xff':
            ret += r'\x{0:02x}'.format(ord(c))
        else:
            ret += c.encode('unicode_escape').decode('ascii')
    return ret

def main():
    if len(sys.argv) != 2:
        raise RuntimeError("Usage: eca <yaml-config-file>")
    config = eca.config.Config(sys.argv[1])

    logging.basicConfig(level=logging.WARNING)

    # Collect all incident timestamps.
    timestamps: TimestampDB = TimestampDB(range=config.range)
    for es in config.event_sources(master=True):
        for ts, line in es.get_events():
            timestamps.append(ts)

    # Collect all texts and if they are applicable order into either within or outside
    # event timestamps.
    texts_within = defaultdict(int)  # Counters for number of times a text appears in the zone
    texts_outside = defaultdict(int)  # Counters for number of times a text appears outside the zone
    texts_not_applicable = defaultdict(int)
    for es in config.event_sources(master=False):
        for ts, line in es.get_events():
            line = es.normalize(line)
            if timestamps.is_applicable(ts):
                if timestamps.in_range(ts):
                    texts_within[line] += 1
                    logging.debug(f"inside:  {ts} - {line[:80]}")
                else:
                    texts_outside[line] += 1
                    logging.debug(f"outside: {ts} - {line[:80]}")
            else:
                texts_not_applicable[line] += 1

    # Find texts that only occur close to incident events but not otherwise and has at least
    # percentile percent number of hits from total incident events.
    min_count = int((len(timestamps) * config.percentile) / 100)
    logging.info(f"min_count:{min_count}")
    print("Normalized texts occurring during incident event zone that matches accuracy and percentile settings:")
    print("---------------------------------------------------------------------------------------------------")
    for txt, count in sorted(texts_within.items(), key=lambda x: x[1], reverse=True):
        printable = escape(txt)
        total_occurrences = texts_outside[txt] + count
        logging.info(f"{printable[20:60]} : total_occurrences:{total_occurrences} count:{count}")

        if int((count * 100) / total_occurrences) >= config.accuracy and count >= min_count:
            print(f"within zone:{count} occurrences, out of zone: {texts_outside[txt]}:\n{printable}\n")
    print("---------------------------------------------------------------------------------------------------")

    print(f"Total {len(timestamps)} incidents, "
          f"{len(texts_within)} texts found within event range, "
          f"{len(texts_outside)} outside. "
          f"{len(texts_not_applicable)} not applicable.")


if __name__ == "__main__":
    main()
