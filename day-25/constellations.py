#! /usr/bin/env python

import sys
from collections import namedtuple, deque
from itertools import product

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

Point = namedtuple("Point", "x y z t")

def distance(a, b):
    return sum(abs(a[i]-b[i]) for i in range(4))

def distance_constellation(a, constellation):
    return min(distance(a,b) for b in constellation)

def is_constellation(a,b):
    return any(distance(i,j)<=3 for (i,j) in product(a,b))

constellations = deque([])
for l in lines:
    pt = Point(*map(int, l.split(',')))
    for c in constellations:
        if distance_constellation(pt, c)<=3:
            c.add(pt)
            break
    else:
        constellations.append(set((pt, )))

result = []
while constellations:
    a = constellations.popleft()
    for b in constellations:
        if is_constellation(a,b):
            b.update(a)
            break
    else:
        result.append(a)

print("Part 1:", len(result))
