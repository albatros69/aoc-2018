#! /usr/bin/env python

import sys
from collections import defaultdict, deque
from typing import DefaultDict, Tuple

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

class Ground():
    scan: DefaultDict
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    source: Tuple[int]

    def __init__(self, lines) -> None:
        self.scan = defaultdict(lambda: '.')
        for l in lines:
            self.add_slice(l)

        self.min_x, self.max_x = 500, 500
        self.min_y, self.max_y = 1000, 0
        for (x, y) in self.scan.keys():
            self.min_x, self.max_x = min(self.min_x, x), max(self.max_x, x)
            self.min_y, self.max_y = min(self.min_y, y), max(self.max_y, y)

        self.source=500,0
        self.scan[self.source]='+'

    def add_slice(self, reading):
        (coord1, val), (coord2, interval) = map(lambda s: s.split('='), reading.split(', '))
        start, end = interval.split('..')
        points=[]
        for i in range(int(start), int(end)+1):
            points.append({coord1: int(val), coord2: i})

        for p in points:
            self.scan[p['x'], p['y']] = '#'

    def __repr__(self):
        return "\n".join(''.join(self.scan[x,y] for x in range(self.min_x-1, self.max_x+2)) for y in range(self.max_y+1))

    def flood(self, mark_fall=False):
        queue=deque([self.source])
        seen=set()
        choices=set()
        falls=[]

        while queue:
            x,y = queue.popleft()

            if y>self.max_y:
                continue

            seen.add((x,y))
            if mark_fall and self.scan[x,y]=='.' and y>=self.min_y:
                self.scan[x,y]='|'

            if self.scan[x,y+1]=='.':
                queue.append((x,y+1))
            elif self.scan[x,y+1]=='~':
                if self.scan[x,y]=='.':
                    choices.add((x,y))
                for i in (-1,1):
                    if self.scan[x+i,y] in '~.' and (x+i,y) not in seen:
                        queue.appendleft((x+i,y))
            else: # self.scan[x,y+1] == '#':
                if self.scan[x,y]=='.':
                    choices.add((x,y))
                for i in (-1,1):
                    if self.scan[x+i,y] in '~.' and (x+i,y) not in seen:
                        queue.appendleft((x+i,y))
                        if self.scan[x+i,y+1]=='.':
                            falls.append((x,y,-i))

        for (x,y,i) in falls: # remove choices contiguous to a fall
            while (x,y) in choices:
                choices.discard((x,y))
                x+=i
        if len(choices)>0:
            for p in choices:
                self.scan[p]='~'
            return True

        return False

    def flooded(self):
        return sum(int(self.scan[p] in '|~') for p in self.scan)
    def retained(self):
        return sum(int(self.scan[p]=='~') for p in self.scan)


ground = Ground(lines)
# print(ground)
while ground.flood():
    pass
    # print(ground)
ground.flood(mark_fall=True)
# print(ground)
print("Part 1:", ground.flooded())
print("Part 2:", ground.retained())
