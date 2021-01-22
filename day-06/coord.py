#! /usr/bin/env python

import sys
from collections import namedtuple
from itertools import product
from heapq import nsmallest

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

Point = namedtuple("Point", ("x", "y"))

points = []
for l in lines:
    x,y = map(int, l.split(','))
    points.append(Point(x,y))

def distance(a,b):
    return abs(b.x-a.x)+abs(b.y-a.y)

frontiers = min(a.x for a in points), max(a.x for a in points), \
            min(a.y for a in points), max(a.y for a in points)
def is_inner(p):
    return frontiers[0]< p.x <frontiers[1] and frontiers[2]< p.y <frontiers[3]

def neighbours(pt):
    return (Point(pt.x+1,pt.y), Point(pt.x-1,pt.y), Point(pt.x,pt.y+1), Point(pt.x,pt.y-1), )

# Part 1
neigh_counts = { p: 0 for p in points if is_inner(p) }
for (x,y) in product(range(frontiers[0], frontiers[1]+1), range(frontiers[2], frontiers[3]+1)):
    p1, p2 = nsmallest(2, points, key=lambda p: distance(Point(x,y), p))
    if p1 in neigh_counts and distance(Point(x,y),p1) < distance(Point(x,y),p2):
        if not is_inner(Point(x,y)):
            del neigh_counts[p1]
        else:
            neigh_counts[p1]+=1

print('Part 1:', max(neigh_counts.values()))

# Part 2
limit=10000
region_size = { p: 0 for p in points if is_inner(p) }
seen=set()
for point in region_size:
    queue = [ point ]
    while queue:
        pt = queue.pop(0)
        if is_inner(pt) and pt not in seen and sum(distance(pt,p) for p in points) < limit:
            region_size[point]+=1
            queue.extend(neighbours(pt))
        seen.add(pt)

print("Part 2:", max(region_size.values()))
