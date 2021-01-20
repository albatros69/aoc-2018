#! /usr/bin/env python

import sys
from collections import Counter
from itertools import combinations

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

# Part 1
result = { 2: 0, 3: 0}
for box in lines:
    c = Counter(box)
    for i in result:
        result[i] += int(any(v==i for v in c.values()))
print('Checksum:', result[2]*result[3])

# Part 2
def distance(s, t):
    d=0
    for i,c in enumerate(s):
        if c!=t[i]:
            d+=1
    return d

for a,b in combinations(lines, 2):
    if distance(a,b)<=1:
        print("Close IDs:", a,b, ''.join(c for c in a if c in b))
        break
