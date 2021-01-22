#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


class Header():
    childs=None
    metadata=None

    def __init__(self, childs, metadata) -> None:
        self.childs = childs
        self.metadata = metadata

    def __len__(self):
        return sum(map(len, self.childs)) + len(self.metadata)

    def sum_metadata(self):
        return sum(self.metadata) + sum(child.sum_metadata() for child in self.childs)

    def value(self):
        if not self.childs:
            return sum(self.metadata)
        else:
            return sum(self.childs[i-1].value() if i<=len(self.childs) else 0 for i in self.metadata)


def read_header(header):
    nb_childs, nb_metadata, *rest = header
    if nb_childs==0:
        return Header([], rest[:nb_metadata]), rest[nb_metadata:]
    else:
        childs = []
        for _ in range(nb_childs):
            child, rest = read_header(rest)
            childs.append(child)
        return Header(childs, rest[:nb_metadata]), rest[nb_metadata:]


header, _ = read_header(list(map(int, lines[0].split(' '))))

print("Part 1:", header.sum_metadata())
print("Part 2:", header.value())
