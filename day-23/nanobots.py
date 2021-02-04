#! /usr/bin/env python

import sys
from collections import namedtuple
from operator import attrgetter
from heapq import heappop, heappush

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

Bot = namedtuple("NanoBot", ("x", "y", "z", "r"))

nanobots = []
for l in lines:
    pos, radius = l.split(', ')
    x,y,z = map(int, pos[5:-1].split(','))
    r = int(radius[2:])
    nanobots.append(Bot(x,y,z,r))

def distance(a,b):
    return sum(abs(a[i]-b[i]) for i in range(3))

# Part 1
strongest = max(nanobots, key=attrgetter('r'))
print("Part 1:", sum(distance(strongest,b)<=strongest.r for b in nanobots))

# Part 2
# Based on an idea found at https://www.reddit.com/r/adventofcode/comments/a8s17l/2018_day_23_solutions/ecfkmyo/?context=8&depth=9
queue = []
for b in nanobots:
    d = distance(b, (0, )*3)
    heappush(queue, (d-b.r, 1))
    heappush(queue, (d+b.r+1, -1))

count=0
maxi=0
result= 0
while queue:
    d, e = heappop(queue)
    count+=e
    if count>maxi:
        result=d
        maxi=count

print("Part 2:", result)