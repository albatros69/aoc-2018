#! /usr/bin/env python

from itertools import product
from multiprocessing import Pool
from collections import defaultdict


def power_level(grid_sn, x,y):
    rack_id = x+10
    return ((rack_id*(rack_id*y+grid_sn))//100)%10 - 5

# Test
# print(power_level(  3,  5,  8)) # 4
# print(power_level(122, 79, 57)) #-5
# print(power_level(217,196, 39)) # 0
# print(power_level(101,153, 71)) # 4

# grid_serial_number = 18
# grid_serial_number = 42
grid_serial_number = 9445

# We tabulate the power of all the cells right and below (x,y)
power_values_square = defaultdict(int)
for (x,y) in product(range(300, 0, -1), range(300, 0, -1)):
    power_values_square[x,y] = power_level(grid_serial_number, x,y)+power_values_square[x,y+1]+power_values_square[x+1,y]-power_values_square[x+1,y+1]


def power_level_square(x,y,size):
    return (power_values_square[x,y]-power_values_square[x+size,y]-power_values_square[x,y+size]+power_values_square[x+size,y+size], x, y, size)


def max_power_level_square(pt):
    x,y=pt
    return max(power_level_square(x,y, size) for size in range(1,302-max(x,y)))


# Part 1
# grid_serial_number = 18 -> (33,45) 29
# grid_serial_number = 42 -> (21,61) 30

max_square_power, x,y, _ = max(power_level_square(x,y,3) for (x,y) in product(range(1,298), range(1,298)))
print("Part 1:", f"{x},{y}", "->", max_square_power)

# Part 2
# grid_serial_number = 18 -> ( 90,269,16) 113
# grid_serial_number = 42 -> (232,251,12) 119

p=Pool()
max_power, x,y,size = max(p.imap_unordered(max_power_level_square, product(range(1,301), range(1,301))))
p.close()
print("Part 2:", "{0},{1},{2}".format(x,y,size), "->", max_power)
