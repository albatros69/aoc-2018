#! /usr/bin/env python

import sys
import re
from collections import defaultdict, namedtuple

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


Point = namedtuple("Point", ("x", "y"))

class Star():
    position=None
    velocity=None

    def __init__(self, x, y, vx, vy) -> None:
        self.position = Point(int(x), int(y))
        self.velocity = Point(int(vx), int(vy))

    def move(self, seconds):
        self.position = Point(self.position.x+seconds*self.velocity.x, self.position.y+seconds*self.velocity.y)


def bounding_box(sky):
    min_x, min_y, max_x, max_y = None, None, None, None
    for star in sky:
        if min_x is not None:
            min_x, min_y = min(min_x, star.position.x), min(min_y, star.position.y)
            max_x, max_y = max(max_x, star.position.x), max(max_y, star.position.y)
        else:
            min_x, min_y = star.position.x, star.position.y
            max_x, max_y = star.position.x, star.position.y

    return Point(min_x, min_y), Point(max_x, max_y)

def surface(sky):
    top_left, bot_right = bounding_box(sky)
    return (bot_right.x-top_left.x)*(bot_right.y-top_left.y)

def print_sky(stars):
    top_left, bot_right = bounding_box(stars)
    sky = defaultdict(lambda : '░')
    for star in stars:
        sky[star.position.x,star.position.y] = '█'
    for y in range(top_left.y, bot_right.y+1):
        for x in range(top_left.x, bot_right.x+1):
            print(sky[x,y], end='')
        print()


re_line = re.compile(r"^position=< *(?P<x>[0-9-]+), *(?P<y>[0-9-]+)> velocity=< *(?P<vx>[0-9-]+), *(?P<vy>[0-9-]+)>$")
stars = []
for l in lines:
    m = re_line.match(l)
    stars.append(Star(m.group("x"), m.group("y"), m.group("vx"), m.group("vy")))
# print_sky(stars)

steps=10000
old_size=surface(stars)
seconds=0
while steps:
    seconds+=steps
    for star in stars:
        star.move(steps)
    size=surface(stars)
    if (size-old_size)>=0:
        steps=-(steps//2)
    old_size=size

seconds-=1
for star in stars:
    star.move(-1)

print_sky(stars)
print('Time:', seconds)
