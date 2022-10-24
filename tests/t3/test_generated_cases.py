#!/usr/bin/env python3

"""
Craft some event files to make test find interesting lines.
"""

from datetime import datetime, timedelta


if __name__ == "__main__":

    ts = datetime.now() - timedelta(weeks=1)

    with open("tests/t3/events.log", "w") as events, open("tests/t3/errors", "w") as errors:
        for i in range(100):
            print(f"{ts} - normal message", file=errors)
            if i % 5 == 0:
                print(f"{ts + timedelta(seconds=2)} - error event occured", file=events)
                print(f"{ts} - some special text every fiths", file=errors)
            elif i % 7 == 0:
                print(f"{ts - timedelta(seconds=2)} - error event occured", file=events)
                print(f"{ts} - some special text every seventh", file=errors)

            ts += timedelta(minutes=4, seconds=13)

