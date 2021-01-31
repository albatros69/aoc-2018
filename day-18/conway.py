#! /usr/bin/env python

import sys
from collections import defaultdict, Counter
from itertools import product
from typing import DefaultDict

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

class Forest():
    state: DefaultDict
    width: int
    height: int
    minute: int

    def __init__(self, lines) -> None:
        self.state=defaultdict(lambda: '.')
        self.height=len(lines)
        for y,l in enumerate(lines):
            self.width=len(l)
            for x,c in enumerate(l):
                self.state[x,y]=c
        self.minute=0

    def neigh_states(self, x,y):
        return Counter(self.state[x+i,y+j] for (i,j)
                        in ((0,1),(0,-1),(1,0),(1,1),(1,-1),(-1,0),(-1,1),(-1,-1),))

    def change(self):
        self.minute+=1
        new_state = self.state.copy()

        for (x,y) in product(range(self.width), range(self.height)):
            neigh_states = self.neigh_states(x,y)
            if self.state[x,y]=='.' and neigh_states['|']>=3:
                new_state[x,y]='|'
            elif self.state[x,y]=='|' and neigh_states['#']>=3:
                new_state[x,y]='#'
            elif self.state[x,y]=='#' and (neigh_states['#']<1 or neigh_states['|']<1):
                new_state[x,y]='.'

        self.state = new_state

    def __repr__(self) -> str:
        return "\n".join(''.join(self.state[x,y] for x in range(self.width)) for y in range(self.height))

    @property
    def nb_trees(self):
        return sum(self.state[x,y]=='|' for (x,y) in product(range(self.width), range(self.height)))
    @property
    def nb_lumberyards(self):
        return sum(self.state[x,y]=='#' for (x,y) in product(range(self.width), range(self.height)))


forest = Forest(lines)
# print(forest)
for _ in range(10):
    forest.change()
    # print(f"After {forest.minute} minutes:", forest, sep='\n')

print('Part 1:', forest.nb_trees*forest.nb_lumberyards)

seen = dict()
limit = 1000000000
while forest.minute < limit:
    forest.change()
    if repr(forest) in seen:
        period = forest.minute-seen[repr(forest)]
        forest.minute += ((limit-forest.minute)//period)*period
        seen.clear() # to finish properly the remaining steps
    else:
        seen[repr(forest)] = forest.minute

print('Part 2:', forest.nb_trees*forest.nb_lumberyards)
