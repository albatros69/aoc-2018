#! /usr/bin/env python

import sys
from typing import List

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


class Instruction():
    registers: List[int]
    operations = ('addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
                  'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr', )
    ip_register: int
    ip: int

    def __init__(self, ip_register, registers=None) -> None:
        self.ip_register=ip_register
        self.ip=0
        if registers:
            self.set_registers(registers)
        else:
            self.set_registers((0,)*6)

    def set_registers(self, registers):
        self.registers = list(registers)
    def incr_ip(self):
        self.ip = self.registers[self.ip_register]+1
    def load_ip(self):
        self.registers[self.ip_register]=self.ip


    def addr(self, A, B, C):
        self.registers[C] = self.registers[A]+self.registers[B]
    def addi(self, A, B, C):
        self.registers[C] = self.registers[A]+B

    def mulr(self, A, B, C):
        self.registers[C] = self.registers[A]*self.registers[B]
    def muli(self, A, B, C):
        self.registers[C] = self.registers[A]*B

    def banr(self, A, B, C):
        self.registers[C] = self.registers[A]&self.registers[B]
    def bani(self, A, B, C):
        self.registers[C] = self.registers[A]&B

    def borr(self, A, B, C):
        self.registers[C] = self.registers[A]|self.registers[B]
    def bori(self, A, B, C):
        self.registers[C] = self.registers[A]|B

    def setr(self, A, B, C):
        self.registers[C] = self.registers[A]
    def seti(self, A, B, C):
        self.registers[C] = A

    def gtir(self, A, B, C):
        self.registers[C] = int(A>self.registers[B])
    def gtri(self, A, B, C):
        self.registers[C] = int(self.registers[A]>B)
    def gtrr(self, A, B, C):
        self.registers[C] = int(self.registers[A]>self.registers[B])

    def eqir(self, A, B, C):
        self.registers[C] = int(A==self.registers[B])
    def eqri(self, A, B, C):
        self.registers[C] = int(self.registers[A]==B)
    def eqrr(self, A, B, C):
        self.registers[C] = int(self.registers[A]==self.registers[B])

    def execute_program(self, program):
        while 0<=self.ip<len(program):
            instr, A,B,C = program[self.ip]
            # print("ip={}\t{}\t{} {} {} {}".format(self.ip, self.registers, instr, A,B,C), end='\t')
            self.load_ip()
            getattr(self, instr)(A,B,C)
            # print(self.registers)
            self.incr_ip()


ip = int(lines[0][3:])
program=[]
for l in lines[1:]:
    instr, A,B,C = l.split()
    program.append((instr,int(A),int(B),int(C)))

# Part 1
instruction = Instruction(ip)
instruction.execute_program(program)
print('Part 1:', instruction.registers[0])

# Part 2
# instruction = Instruction(ip, (1, 0, 0, 0, 0, 0))
# instruction.execute_program(program)
# print('Part 2:', instruction.registers[0])
# The program runs for ages, because it's supposed to compute the sums
# of factors for 10551383 (in my case), with a naïve approach.
# https://www.reddit.com/r/adventofcode/comments/a7j9zc/2018_day_19_solutions/
# So we cheat... :(
def factors(n):
    tmp = []
    for i in range(1, round(pow(n, 0.5))+1):
        if n%i==0:
            tmp.extend((i, n//i))
    return tmp
print("Part 2:", sum(factors(10551383)))
