# Event-Coincident-Analysis
Python project for correlating date/time events listed in two files.

# Usage
eca.py [--verbose] [--overlap <seconds>] file1 file2

Each file should be a time sorted list lines containing UTC ISO-timestamps 
of format like: 2022-10-23T11:22:32.2323Z

By default conincidence  is calculated with 1 second overlap.
