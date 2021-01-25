#! /usr/bin/env python

import sys
from typing import DefaultDict, List
from collections import defaultdict

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


directions = { '^': (0,-1), 'v': (0,1), '>': (1,0), '<': (-1,0) }
# transitions = { '^\\': '<', '^/': '>', 'v\\': '>', 'v/': '<',
#                 '>\\': 'v', '>/': '^', '<\\': '^', '</': 'v', }
transitions = { ((0,-1), '\\'): (-1,0), ((0,-1),'/'): (1, 0), (( 0,1),'\\'): (1, 0), (( 0,1),'/'): (-1,0),
                ((1, 0), '\\'): ( 0,1), ((1, 0),'/'): (0,-1), ((-1,0),'\\'): (0,-1), ((-1,0),'/'): ( 0,1), }

def add(pos, dir):
    return (pos[0]+dir[0], pos[1]+dir[1])

def rotate(dir, angle):
    if angle==(0,0):
        return dir
    else:
        return (dir[1]*angle[0], dir[0]*angle[1])


class Cart():
    position: tuple
    direction: tuple
    angles: list

    def __init__(self, position, direction) -> None:
        self.position = position
        self.direction = directions[direction]
        # left, straight, right
        self.angles = [ (1,-1), (0,0), (-1,1) ]

    def handle_cross(self):
        angle=self.angles.pop(0)
        self.direction=rotate(self.direction, angle)
        self.angles.append(angle)

    def handle_curve(self, curve):
        self.direction=transitions[self.direction, curve]

    def move(self):
        self.position=add(self.position, self.direction)


class Track():
    map: DefaultDict
    width: int
    height: int
    carts: List[Cart]
    tick: int

    def __init__(self, lines, part='part1') -> None:
        self.part=part
        self.tick=0
        self.map=defaultdict(lambda: ' ')

        tmp = { '^': '|', 'v': '|', '<': '-', '>': '-'}
        self.carts=[]
        self.height,self.width=len(lines),0
        for y,l in enumerate(lines):
            self.width=max(self.width, len(l))
            for x,c in enumerate(l):
                if c in '^v<>':
                    self.carts.append(Cart((x,y), c))
                    self.map[x,y]=tmp[c]
                else:
                    self.map[x,y]=c

    def run(self):
        for cart in sorted(self.carts, key=lambda c: (c.position[1],c.position[0])):
            cart.move()
            if any(c.position==cart.position for c in self.carts if c!=cart):
                self.handle_collision(cart.position)
            elif self.map[cart.position]=='+':
                cart.handle_cross()
            elif self.map[cart.position] in '\/':
                cart.handle_curve(self.map[cart.position])
        self.tick+=1

    def handle_collision(self, pos):
        if self.part=='part2' and len(self.carts)>2:
            self.carts = [ c for c in self.carts if c.position!=pos ]
        else:
            raise StopIteration("{0[0]},{0[1]}".format(pos))

    def print(self):
        tmp=self.map.copy()
        dir = { (0,-1): '^', (0,1): 'v', (1,0): '>', (-1,0): '<' }

        for c in self.carts:
            tmp[c.position]=dir[c.direction]
        for y in range(self.height):
            print(''.join(tmp[x,y] for x in range(self.width)))


# Part 1
track=Track(lines)
# track.print()
while True:
    try:
        track.run()
        # track.print()
    except StopIteration as e:
        # track.print()
        print("Part 1:", e)
        break

# Part 2
track=Track(lines, 'part2')
while len(track.carts)>1:
    track.run()
last_cart=track.carts[0] if track.carts else None
print("Part 2:", "{0[0]},{0[1]}".format(last_cart.position))