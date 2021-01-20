#! /usr/bin/env python

import sys
from collections import defaultdict
from datetime import datetime, timedelta, time

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


class Guard():
    id=None
    sleep_schedule=None

    def __init__(self, id) -> None:
        self.id = int(id)
        self.sleep_schedule = defaultdict(int)

    def add_date(self, date, state):
        for m in range(date.minute, 60):
            self.sleep_schedule[m]+= 1 if state=="falls asleep" else -1

    def __repr__(self) -> str:
        return f'Guard #{self.id}'

guard_schedule=dict()
guards=dict()

for l in sorted(lines):
    date, text = l.split(']', 1)
    date = datetime.strptime(date, "[%Y-%m-%d %H:%M")
    if date.hour>=23:
        date = datetime.combine(date.date()+timedelta(days=1), time(hour=0, minute=0))
        start_of_shift = date.timestamp()
    else:
        start_of_shift = datetime(year=date.year, month=date.month, day=date.day, hour=0, minute=0).timestamp()

    if start_of_shift in guard_schedule:
        g=guard_schedule[start_of_shift]
        g.add_date(date, text.strip())
    else:
        guard_id = int(''.join(c for c in text if c.isdigit()))
        if guard_id not in guards:
            guards[guard_id] = Guard(guard_id)
        guard_schedule[start_of_shift] = guards[guard_id]


# Part 1
most_asleep = max(guards.values(), key = lambda g: sum(g.sleep_schedule.values()))
minute_to_pick = max(most_asleep.sleep_schedule, key=lambda g: most_asleep.sleep_schedule[g])
print("Part 1:", most_asleep, "on minute", minute_to_pick, "->", most_asleep.id*minute_to_pick)

# Part 2
most_asleep = max(guards.values(), key = lambda g: max(g.sleep_schedule.values()) if g.sleep_schedule else 0)
minute_to_pick = max(most_asleep.sleep_schedule, key=lambda g: most_asleep.sleep_schedule[g])
print("Part 2:", most_asleep, "on minute", minute_to_pick, "->", most_asleep.id*minute_to_pick)

