#! /usr/bin/env python

import sys
from typing import Dict
from collections import namedtuple, deque
from heapq import heappop, heappush

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


Position = namedtuple("Position", ("x", "y"))
directions = { 'N': Position(0,1), 'S': Position(0,-1), 'E': Position(1,0), 'W': Position(-1,0), }
rev = { 'N':'S', 'S':'N', 'E':'W', 'W':'E' }

State = namedtuple("State", ('re', 'pos', 'outer_stack', 'inner_stack'))

def add(pos, dir):
    if isinstance(dir, str):
        d = directions[dir]
        return Position(pos.x+d.x,pos.y+d.y)
    elif isinstance(dir, (Position, tuple)):
        return Position(pos.x+dir[0], pos.y+dir[1])


class Room():
    position: Position
    neigh: Dict
    state: str

    def __init__(self, x,y, state='.') -> None:
        self.position = Position(x,y)
        self.neigh = dict.fromkeys(directions.keys(), None)
        self.state = state

    def __repr__(self) -> str:
        result= list((list('#?#'), list(f'?{self.state}?'), list('#?#')))
        for k in self.neigh:
            tmp=add(Position(1,1), k)
            if self.neigh[k]:
                result[tmp.y][tmp.x] = '|' if k in 'EW' else '-'
            else:
                result[tmp.y][tmp.x] = '#'
        return '\n'.join(reversed(list(''.join(l) for l in result)))

class Map():
    carto: Dict

    def __init__(self, regex) -> None:
        self.carto = dict()
        self.expand_re(regex)

    def __repr__(self) -> str:
        min_x, max_x = 1000, 0
        min_y, max_y = 1000, 0
        for (x, y) in self.carto.keys():
            min_x, max_x = min(min_x, x), max(max_x, x)
            min_y, max_y = min(min_y, y), max(max_y, y)

        result = []
        for y in range(max_y, min_y-1, -1):
            line = ['', '', '']
            for x in range(min_x, max_x+1):
                for i,r in enumerate(repr(self.carto[x,y]).splitlines()):
                    if line[2]:
                        line[i]+=r[1:]
                    else:
                        line[i]+=r
            if result:
                result.extend(line[1:])
            else:
                result.extend(line)
        return "\n".join(result)

    def expand_re(self, regex):
        queue = deque([ State(regex, Position(0,0), [], []) ])
        self.carto[Position(0,0)] = Room(0,0, state='X')

        while queue :
            state = queue.popleft()

            if state.re=='':
                break
            elif state.re[0]=='(':
                queue.appendleft(State(state.re[1:], state.pos, state.outer_stack+[(state.pos, state.inner_stack[:])], []))
            elif state.re[0]=='|':
                old_pos, _ = state.outer_stack[-1]
                queue.appendleft(State(state.re[1:], old_pos, state.outer_stack[:], state.inner_stack+[state.pos]))
            elif state.re[0]==')':
                _, old_inner_stack = state.outer_stack.pop()
                for branch_pos in state.inner_stack+[state.pos]:
                    queue.appendleft(State(state.re[1:], branch_pos, state.outer_stack[:], old_inner_stack))
            else: # state.re[0] in 'NSEW':
                dir = state.re[0]
                new_pos = add(state.pos, dir)

                if new_pos not in self.carto:
                    self.carto[new_pos] = Room(*new_pos)

                self.carto[state.pos].neigh[dir] = self.carto[new_pos]
                self.carto[new_pos].neigh[rev[dir]] = self.carto[state.pos]
                queue.appendleft(State(state.re[1:], new_pos, state.outer_stack, state.inner_stack))

    def furthest_room(self):
        """ Shortest path to a target """
        queue = [ (0, Position(0,0)) ]

        seen=set()
        count_farthest = 0
        while queue:
            nb_doors, position = heappop(queue)
            count_farthest += int(nb_doors>=1000)
            seen.add(position)
            for d in directions.keys():
                new_room = self.carto[position].neigh[d]
                if new_room and new_room.position not in seen:
                    heappush(queue, (nb_doors+1, new_room.position, ))

        return nb_doors, count_farthest


# Part 1
for l in lines:
    # print(l)
    rooms = Map(l.rstrip('$').lstrip('^'))
    nb_doors, count_farthest = rooms.furthest_room()
    print(f'Furthest room requires passing {nb_doors} doors')
    print(f'{count_farthest} rooms requires crossing 1000+ doors')
    # print(rooms, '-'*8, sep='\n')

