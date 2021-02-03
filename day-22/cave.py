#! /usr/bin/env python

import sys
from itertools import product
from heapq import heappop, heappush

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

depth=int(lines[0].split()[1])
target_X,target_Y=map(int, lines[1].split()[1].split(','))

def print_cave(c):
    region_type = '.=|'
    for y in range(target_Y+1):
        print(''.join(region_type[c[x,y]%3] for x in range(target_X+1)))

cave=dict()
def erosion_level(x,y):
    if (x,y) not in cave:
        if (x,y) in ((0,0), (target_X, target_Y)):
            geologic_index = 0
        elif y==0:
            geologic_index = x*16807
        elif x==0:
            geologic_index = y*48271
        else:
            geologic_index = erosion_level(x-1,y)*erosion_level(x,y-1)

        cave[x,y]=(geologic_index+depth)%20183

    return cave[x,y]

# Part 1
risk_level=0
for (x,y) in product(range(target_X+1), range(target_Y+1)):
    risk_level+=erosion_level(x,y)%3
# print_cave(cave)
print("Part 1:", risk_level)

# Part 2
def add(pos, d):
    return (pos[0]+d[0], pos[1]+d[1])

# eqpt: 0='', 1=='torch', 2='climbing gear'
# rocky = 0  --> eqpt in 1,2
# wet = 1    --> eqpt in 0,2
# narrow = 2 --> eqpt in 0,1

def new_state(time, position, eqpt):
    return (time + position[0] + position[1] + (0 if eqpt==1 else 7), time, position, eqpt)

# We start from the target to always pick from the queue the state closest to the start
queue = [ (target_X+target_Y, 0, (target_X,target_Y), 1) ]
seen=dict()
while queue:
    # The metric is only useful to keep the heap sorted properly
    _, time, position, eqpt = heappop(queue)

    if position==(0,0):
        if eqpt==1:
            break
        else:
            heappush(queue, new_state(time+7, position, 1))
    elif (position, eqpt) in seen and seen[position, eqpt]<=time:
        continue
    else:
        seen[position,eqpt]=time
        for d in ((1, 0),(-1,0),(0, 1),(0,-1)):
            new_pos=add(position, d)
            if (new_pos[0]<0 or new_pos[1]<0):
                continue

            current_type=erosion_level(*position)%3
            new_type=erosion_level(*new_pos)%3
            if eqpt==new_type:
                # new_eqpt can only be the value different from both new_type and current_type
                # to be a compatible transition, thus this formula...
                new_eqpt=3-current_type-new_type
                new_time=time+8
            else:
                new_eqpt=eqpt
                new_time=time+1

            if (new_pos, new_eqpt) not in seen:
                heappush(queue, new_state(new_time, new_pos, new_eqpt))

print("Part 2:", time)
