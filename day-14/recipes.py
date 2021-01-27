#! /usr/bin/env python

# Part 1
input = 633601
# input = 9    # 5158916779
# input = 5    # 0124515891
# input = 18   # 9251071085
# input = 2018 # 5941429882

scoreboard = '37'
elves = [ 0, 1 ]

while len(scoreboard)<=input+10:
    val = 0
    new_elves = elves.copy()
    for i in (0, 1):
        val += int(scoreboard[elves[i]])
        new_elves[i] += 1+int(scoreboard[elves[i]])
    scoreboard+=str(val)
    elves = [ i%len(scoreboard) for i in new_elves ]

print('Part 1:', scoreboard[input:input+10])

# Part 2
# input = '51589' # 9
# input = '01245' # 5
# input = '92510' # 18
# input = '59414' # 2018
input = '633601'

scoreboard = '37'
elves = [ 0, 1 ]

while True:
    val = 0
    new_elves = elves.copy()
    for i in (0, 1):
        val += int(scoreboard[elves[i]])
        new_elves[i] += 1+int(scoreboard[elves[i]])
    scoreboard+=str(val)
    elves = [ i%len(scoreboard) for i in new_elves ]

    if scoreboard[-len(input):]==input or scoreboard[-len(input)-1:-1]==input:
        break

print('Part 2:', scoreboard.find(input))
