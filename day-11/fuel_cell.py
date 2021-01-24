#! /usr/bin/env python

from itertools import product
from multiprocessing import Pool
from functools import partial


def power_level(grid_sn, x,y):
    rack_id = x+10
    return ((rack_id*(rack_id*y+grid_sn))//100)%10 - 5

# Test
# print(power_level(  3,  5,  8)) # 4
# print(power_level(122, 79, 57)) #-5
# print(power_level(217,196, 39)) # 0
# print(power_level(101,153, 71)) # 4


def power_level_square(grid_sn, x,y,size):
    return (sum(power_level(grid_sn, x+i,y+j) for (i,j) in product(range(size), range(size))), x, y, size)


def max_power_level_square(grid_sn, pt):
    x,y=pt
    max_square_power=0
    result=0,0,0
    power=0
    for size in range(1,302-max(x,y)):
        power+=sum(power_level(grid_sn, x+i,y+size-1)+power_level(grid_sn, x+size-1,y+i) for i in range(size-1)) + power_level(grid_sn, x+size-1,y+size-1)
        if power>max_square_power:
            result=x,y,size
            max_square_power=power

    return (max_square_power, *result)


# grid_serial_number = 18 # -> (33, 45) 29
# grid_serial_number = 42 # -> (21, 61) 30
grid_serial_number = 9445

# Part 1
max_square_power, x,y, _ = max(power_level_square(grid_serial_number, x,y,3) for (x,y) in product(range(1,298), range(1,298)))
print("Part 1:", f"{x},{y}", "->", max_square_power)

# Part 2
# grid_serial_number = 18 # -> (90,269,16) 113
# grid_serial_number = 42 # -> (232,251,12) 119

p=Pool()
max_power, x,y,size = max(p.imap_unordered(partial(max_power_level_square, grid_serial_number), product(range(301), range(301))))
p.close()
print("Part 2:", "{0},{1},{2}".format(x,y,size), "->", max_power)
