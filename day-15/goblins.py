#! /usr/bin/env python

import sys
from typing import Dict, List
from operator import attrgetter
from heapq import heappop, heappush

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

def rev(dir):
    return (-dir[0], -dir[1])

def add(pos, dir):
    return (pos[0]+dir[0], pos[1]+dir[1])


class Unit():
    x: int
    y: int
    type: str
    attack_power=3
    hit_points=200

    def __init__(self, y,x, type) -> None:
        self.x, self.y = x, y
        self.type = type

    def is_alive(self):
        return self.hit_points>0

    def neighbours(self):
        return [ (self.y+dy, self.x+dx) for (dy,dx) in ((0,1),(0,-1),(1,0),(-1,0)) ]

    def inrange(self, targets):
        return sorted([ t for t in targets if (t.y,t.x) in self.neighbours() ],
                      key=attrgetter('hit_points','y','x'))

    def attack(self, other):
        other.hit_points -= self.attack_power

    def move(self, y,x):
        self.x=x
        self.y=y

    def __repr__(self) -> str:
        return "{0.type}({0.y},{0.x}): {0.hit_points}".format(self)


class Cave():
    map: Dict
    units: List[Unit]
    width: int
    height: int
    round: int

    def __init__(self, lines) -> None:
        self.round=0
        self.map=dict()
        self.units=[]

        self.height=len(lines)
        self.width=0
        for y,l in enumerate(lines):
            self.width=max(self.width, len(l))
            for x,c in enumerate(l):
                if c in ('G', 'E'):
                    self.units.append(Unit(y,x,c))
                self.map[y,x]=c

    def __repr__(self):
        return "\n".join(''.join(self.map[y,x] for x in range(self.width)) for y in range(self.height))


    def shortest_path(self, unit, targets):
        """ Shortest path to a list of targets """
        queue = [ (0, (unit.y, unit.x), []) ]

        if not targets:
            return None

        seen=set()
        while queue:
            distance, position, path = heappop(queue)
            if position in targets:
                return path
            else:
                for d in ((0,1),(0,-1),(1,0),(-1,0)):
                    new_pos = add(position, d)
                    if new_pos not in seen and self.map[new_pos]=='.':
                        heappush(queue, (distance+1, new_pos, path+[new_pos], ))
                        seen.add(new_pos)

        return None

    def move_order(self, unit, new_pos):
        self.map[unit.y,unit.x]='.'
        unit.move(*new_pos)
        self.map[new_pos]=unit.type

    def attack_order(self, unit, target):
        unit.attack(target)
        if not target.is_alive():
            self.map[target.y,target.x]='.'

    def is_elves_victory(self):
        return all(u.is_alive() for u in self.units if u.type=='E')

    def outcome(self):
        return self.round*sum(u.hit_points for u in self.units if u.is_alive())

    def turn(self):
        self.units.sort(key=attrgetter('y','x'))

        for unit in (u for u in self.units if u.is_alive()):
            targets=[ u for u in self.units if u.type!=unit.type and u.is_alive() ]
            if len(targets)==0:
                raise StopIteration

            targets_inrange = unit.inrange(targets)
            if targets_inrange:
                self.attack_order(unit, targets_inrange[0])
            else:
                path = self.shortest_path(unit, [ pt for t in targets for pt in t.neighbours() if self.map[pt]=='.' ])
                if path:
                    self.move_order(unit, path[0])
                    targets_inrange = unit.inrange(targets)
                    if targets_inrange:
                        self.attack_order(unit, targets_inrange[0])

        self.round+=1


# Part 1
battle = Cave(lines)
# print(battle)

try:
    while True:
        battle.turn()
    # print("Round:", battle.round); print(battle)
except StopIteration:
    # print(battle)
    print("Part 1:", battle.outcome())

# Part 2
step=10
attack_power=3
past_victory=battle.is_elves_victory()

while step!=0:
    battle = Cave(lines)

    attack_power+=step
    for elve in (u for u in battle.units if u.type=='E'):
        elve.attack_power=attack_power

    try:
        while True:
            battle.turn()
    except StopIteration:
        if past_victory!=battle.is_elves_victory():
            step=-(step//2)
        past_victory=battle.is_elves_victory()

print("Part 2:", battle.outcome())
