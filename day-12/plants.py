#! /usr/bin/env python

import sys
from collections import defaultdict

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

pots=defaultdict(lambda:'.')
for i,c in enumerate(lines[0].split(' ')[2]+'..'):
    pots[i]=c
pots[-1]='.';pots[-2]='.' # We need this to start properly to check for patterns

rules=[]
for l in lines[2:]:
    pattern, new_state = l.split(' => ')
    if new_state=='#':
        rules.append({ i-2: c for (i,c) in enumerate(pattern)})


def apply_rules(state):
    new_state=state.copy()

    for k in new_state.keys():
        if any(all(state[k+i]==p[i] for i in p) for p in rules):
            new_state[k]='#'
        else:
            new_state[k]='.'

    # This is to strip the leading and trailing '.....' that won't change anyway,
    # and thus reduce the state length
    return defaultdict(lambda:'.', ((k, new_state[k])
        for k in state if ''.join(new_state[k+j] for j in range(-2,3))!='.....'))

def print_state(state):
    print(''.join(state[k] for k in sorted(state.keys())))


# Part 1
state=pots.copy()
# print(" 0:", end=' '); print_state(state)
for i in range(20):
    state=apply_rules(state)
    # print(f"{i+1:2d}:", end=' '); print_state(state)
print("Part 1:", sum(k for k in state if state[k]=='#'))

# Part 2
# Running for so long is unfeasible. But if you look closer to the evolution,
# we can see that we're dealing with a spaceship (https://en.wikipedia.org/wiki/Spaceship_(cellular_automaton))
# Meaning, we need to detect the point in time when we "launch" then just offset the position of
# the spaceship till the time limit.
state=pots.copy()
limit=50000000000
seen=set()
i=0
while i<limit:
    i+=1
    # print(f"{i:2d}:", min(state.keys()), len(state), end=' '); print_state(state)
    state=apply_rules(state)
    if ''.join(state.values()) in seen:
        break
    seen.add(''.join(state.values()))

print("Part 2:", sum(k+limit-i for k in state if state[k]=='#'))
