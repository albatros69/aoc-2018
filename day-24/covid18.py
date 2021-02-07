#! /usr/bin/env python

import sys
import re
from collections import Counter
from copy import deepcopy
from typing import Tuple

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


class Group():
    type: str
    nb_units: int
    hit_points: int
    weaknesses: Tuple[str]
    immunities: Tuple[str]
    damage_points: int
    damage_type: str
    initiative: int

    def __init__(self, type, nb_units, hp, qualities, dp, attack, initative) -> None:
        self.type=type.lower()
        self.nb_units=int(nb_units)
        self.hit_points = int(hp)
        self.damage_points = int(dp)
        self.damage_type = attack.lower()
        self.initiative = int(initative)

        self.immunities= tuple()
        self.weaknesses = tuple()
        for q in qualities.strip(' ()').split('; '):
            if q.startswith('weak to'):
                self.weaknesses = tuple(w.lower() for w in q[8:].split(', '))
            elif q.startswith('immune to'):
                self.immunities = tuple(i.lower() for i in q[10:].split(', '))

    def __repr__(self) -> str:
        return "Group {0.type}: {0.nb_units} units @{0.hit_points} (immune to {1}; weak to {2}) " \
               "{0.damage_points} {0.damage_type} at {0.initiative}".format(
                   self, ', '.join(self.immunities), ', '.join(self.weaknesses))
        # return "Group {0.type}: {0.nb_units}".format(self)

    @property
    def effective_power(self):
        return self.nb_units*self.damage_points

    def damage(self, other):
        if self.damage_type in other.immunities:
            return 0
        else:
            return self.effective_power*(2 if self.damage_type in other.weaknesses else 1)

    def deal_damage(self, defender):
        if defender:
            defender.nb_units = max(0, defender.nb_units - self.damage(defender)//defender.hit_points)


reindeer = []
type = ''
re_group = re.compile(r"(?P<nb_units>\d+) units each with (?P<hp>\d+) hit points (?P<qualities>.*)with an " \
                      r"attack that does (?P<dp>\d+) (?P<attack>\w+) damage at initiative (?P<initiative>\d+)$")
for l in lines:
    if not l:
        continue
    elif l[-1]==':':
        type=l[:-1]
    else:
        m = re_group.match(l)
        reindeer.append(Group(type, m.group('nb_units'), m.group('hp'), m.group('qualities'),
                              m.group('dp'), m.group('attack'), m.group('initiative')))

def battle(subject):

    monit = 0 # needed in case all the effective powers are lower than the hit points (-> infinite loop)
    while True:
        # Target selection
        targets = dict()
        for g in sorted((g for g in subject if g.nb_units>0),
                        key=lambda g: (g.effective_power, g.initiative), reverse=True):
            targets[g] = None
            foes = sorted((other for other in subject
                        if other.type!=g.type and other.nb_units>0 and g.damage(other)>0 and other not in targets.values()),
                        key=lambda o: (g.damage(o), o.effective_power, o.initiative), reverse=True)
            if foes:
                targets[g] = foes[0]

        # Attacking
        for (attacker, defender) in sorted(targets.items(), key=lambda a: a[0].initiative, reverse=True):
            attacker.deal_damage(defender)

        tmp = Counter()
        for g in subject:
            tmp.update({ g.type: g.nb_units})
        if any(tmp[c]==0 for c in tmp) or monit==sum(tmp.values()):
            break
        monit = sum(tmp.values())

    return tmp


print("Part 1:", battle(deepcopy(reindeer)))

# Part 2
boost=0
step=10
past_victory = False

while step!=0:
    tentative = deepcopy(reindeer)

    boost+=step
    for immune_sys in (g for g in tentative if g.type=='immune system'):
        immune_sys.damage_points+=boost

    tmp = battle(tentative)
    if past_victory!=(tmp['immune system']>0 and tmp['infection']==0):
        step=-(step//2)
    past_victory=tmp['immune system']>0 and tmp['infection']==0

print("Part 2:", boost, "-->", tmp)

