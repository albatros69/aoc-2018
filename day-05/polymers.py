#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

def reduce(polymer, filter=''):
    if len(polymer)<=1:
        return polymer if polymer.lower()!=filter else ''

    result=''
    for c in polymer:
        if c.lower()==filter:
            pass
        elif result and c==result[-1].swapcase():
            result=result[:-1]
        else:
            result+=c

    return result

# Test
polymer_test='dabAcCaCBAcCcaDA'

# Part 1
polymer=lines[0]
print("Part 1:", len(reduce(polymer)))

# Part 2
polymer=lines[0]
print("Part 2:", min(len(reduce(polymer, filter=c)) for c in 'abcdefghijklmnopqrstuvwxyz'))