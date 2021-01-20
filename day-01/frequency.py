#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

frequency=0
seen=set()

# Part 1
for adjustement in map(int, lines):
    seen.add(frequency)
    frequency+=adjustement
    if frequency in seen:
        print('Duplicate frequency (Part 2):', frequency)
print("Resulting frequency (Part 1):", frequency)

# Part 2
while True:
    for adjustement in map(int, lines):
        seen.add(frequency)
        frequency+=adjustement
        if frequency in seen:
            print('Duplicate frequency (Part 2):', frequency)
            raise StopIteration
