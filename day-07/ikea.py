#! /usr/bin/env python

import sys
from bisect import insort
from heapq import heappop, heappush

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

class Step():
    name=None
    childrens=None
    parents=None

    def __init__(self, name) -> None:
        self.name=name.upper()
        self.childrens=[]
        self.parents=[]

    def add_step(self, child):
        self.childrens.append(child)
        child.parents.append(self)


steps = dict()
for l in lines:
    step, child = map(lambda c: c.upper(), (l[5], l[-12]))
    if step not in steps:
        steps[step] = Step(step)
    if child not in steps:
        steps[child] = Step(child)
    steps[step].add_step(steps[child])


# Part 1
ready = [ ]
for s in steps.values():
    if not s.parents:
        insort(ready, s.name)

waiting = set()
done = ''

while ready:
    step = ready.pop(0)
    done += step

    for s in steps[step].childrens:
        if all(p.name in done for p in s.parents) and s.name not in ready:
            insort(ready, s.name)
        else:
            waiting.add(s.name)

    for c in waiting:
        s = steps[c]
        if all(p.name in done for p in s.parents) and c not in ready:
            insort(ready, s.name)
    waiting = waiting-set(ready)

print("Part 1:", done)

# Part 2
def duree(s):
    # ord('A')=65 --> -4 = 60 - 65 + 1
    return ord(s)-4

time = 0
done = ''
ready = set( s.name for s in steps.values() if not s.parents )
running = set()
waiting = set()
queue = [ (time, done, ready, running, waiting ) ]

while ready or running or waiting:
    time, done, ready, running, waiting = heappop(queue)
    if len(done)==len(steps):
        break
    elif len(running)<5 and ready:
        for s in ready:
            heappush(queue, (time, done, ready-set((s, )), running|set(((time+duree(s), s), )), waiting))
    elif running:
        finish, c = min(running)
        step = steps[c]
        new_done = done+step.name
        new_waiting = waiting|set(s.name for s in step.childrens)
        new_ready = ready|set( s for s in new_waiting if all(p.name in new_done for p in steps[s].parents))
        heappush(queue, (finish, new_done, new_ready, running-set(((finish, c), )), new_waiting-new_ready))
    else:
        raise StopIteration

print("Part 2:", done, "in", time)
