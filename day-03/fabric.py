#! /usr/bin/env python

import sys
from itertools import product
from collections import defaultdict

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

# Part 1
fabric=defaultdict(int)
for l in lines:
    id, _, top_left, dim = l.split(' ')
    id=int(id[1:])
    col,row = map(int, top_left[:-1].split(','))
    w,h = map(int, dim.split('x'))
    for (i,j) in product(range(w),range(h)):
        fabric[col+i,row+j]+=1

print("Claim conflicts:", sum(v>1 for v in fabric.values()))

# Part 2
for l in lines:
    id, _, top_left, dim = l.split(' ')
    id=int(id[1:])
    col,row = map(int, top_left[:-1].split(','))
    w,h = map(int, dim.split('x'))
    if all(fabric[col+i,row+j]==1 for (i,j) in product(range(w),range(h))):
        print("Claim with no conflict", id)
        break
