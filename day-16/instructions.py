#! /usr/bin/env python

import sys
from typing import List
from collections import defaultdict

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


class Instruction():
    registers: List[int]
    operations = ('addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
                  'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr', )

    def __init__(self, registers=None) -> None:
        if registers:
            self.set_registers(registers)
        else:
            self.set_registers((0,)*4)

    def set_registers(self, registers):
        self.registers = list(registers)

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


# Part 1
samples=defaultdict(set)
instruction = Instruction()
test_programs = []
for l in range(0, len(lines), 4):
    before,instr,after = lines[l:l+3]
    if before.startswith('Before:'):
        before = list(map(int, before[9:-1].split(', ')))
        after = list(map(int, after[9:-1].split(', ')))
        opcode, A,B,C = map(int, instr.split())
        for i in instruction.operations:
            instruction.set_registers(before)
            getattr(instruction, i)(A,B,C)
            if instruction.registers == after:
                samples[l, opcode].add(i)
    else:
        test_programs = lines[l+2:]
        break

print('Part 1:', sum(len(v)>=3 for v in samples.values()))

# Part 2
alternatives = sorted(samples.items(), key=lambda x: len(x[1]))
trans_table = dict()
while len(trans_table)<len(Instruction.operations):
    for ((_,o), i) in alternatives:
        tmp = list(k for k in i if k not in trans_table.values())
        if len(tmp)==1:
            trans_table[o]=tmp[0]

instruction = Instruction()
for i in test_programs:
    opcode, A,B,C = map(int, i.split())
    getattr(instruction, trans_table[opcode])(A,B,C)

print("Part 2:", instruction.registers[0])
