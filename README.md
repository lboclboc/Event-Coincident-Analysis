# Event-Coincident-Analysis
Python project for correlating date/time events

# Usage
eca.py [--verbose] [--overlap <seconds>] file1 file2

Each file should be a time sorted list lines containing UTC ISO-timestamps
of format like: 2022-10-23T11:22:32.2323Z

By default conincidence  is calculated with 1 second overlap.

# Terminology
- MasterEvents   - The list of events where incidents ocurred.
- TextEvents     - Event log with textual information
- MetricValues   - Continous values
- EventSource    - Sore for event information to examine, like TextEvents or MetricValues
- EventCategory  - Each EventSource can be assigned an EventCategory for grouping matches.

# Supported timeformats:
- 2022-10-20T04:33:05.328430Z

# Yaml config syntax:
# Time range during which incident events are considered to coincide. The time span
# for an incident event is this its parsed start time until start time + this range.
range: 1s

# Only include texts that is present in this percent of incident events.
# If 90 cases of a text was found inside incident time span, then a percentil of 90
# will include those texts.
percentile: 90

# Number of texts that must occur inside incident time span in percent of total occurences.
# If a text occurs 100 times in total, and 80 of them during incident time span, then a skew
# of 80 will include those texts.
skew: 90

# List of event sources. Event sources where master is set to true is considered to be a source
# of incident events, the text part of master files are ignored.
sources:
- filename: name
  categories: [categories]
  master: <true/false>
  type: text-events
  date-format: <auto|iso|"{year:4}...">
  timezone: <+/- hours>
  default-date: <default date for non date timestamps>
  default-time: <default start time for time delta timestamps>
  normalizers: [remove-digits]

# TODO
Support time ranges from the file.

Warn about lines not containing timestamps

Examine first part of file to determine time stamp format

Find patterns that conicide with the events but not outside the events. As a percentage match.

Dates in logfiles before the first event should be discarded since they may turn up as matches in good time spans.

yaml-based input with info like:
- tags for file
- start-time for relative timestamps
- timezone for stamps without zone-info
- force format
- year if that is missing
- date if that is missing

Support timeformats:
- 2022-10-20T04:33:05.328430+00:00
- [2021-02-21T11:50:50.670055 #11280]
- 2022-10-06 06:32:52
- 2022-10-04 16:03:34,351
- [2020-09-28 17:56:12 +0200]
- [2021-02-22 18:51:37,108]
- 2022-10-17 12:34:23.930+0000
- 2022-03-07 11:14:28 CET
- 2020/08/24 10:06:13.163
- 2022-10-07  06:29:48
- 20221016:000003.093
- 20221020_043225

- Oct 20 00:06:29
- Sat Apr 10 02:52:06 CEST 2021
- Wed Oct 19 16:26:39 2022
- (Mon Sep  5 11:00:31 2022)
- [20/Oct/2022:00:00:02 +0200]

- [ 04:33:07.739 ]
- 08:14:00.769

- [3843994.198557]
- [    0.002295]  (relative timestamp)
- [+13.38s]
