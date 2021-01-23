#! /usr/bin/env python

import sys
from collections import deque, defaultdict


lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


def play(nb_players, last_marble):
    circle = deque([ 0 ])
    scores = defaultdict(int)

    for marble in range(1, last_marble+1):
        if marble%23==0:
            circle.rotate(-7)
            player = marble%nb_players
            scores[player]+=marble+circle.pop()
        else:
            circle.rotate(2)
            circle.append(marble)

    return max(scores.values())


for l in lines:
    tmp = l.split(' ')
    nb_players, last_marble = int(tmp[0]), int(tmp[6])

    print("Part 1:", l+".", "High score is", play(nb_players, last_marble))
    print("Part 2:", l+".", "High score is", play(nb_players, 100*last_marble))