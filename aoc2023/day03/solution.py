"""AOC 2023 Day 3 solutions."""

import re
from typing import Iterator, NamedTuple, Optional


class Coord(NamedTuple):
    r: int
    c: int

    def neighbors(self) -> Iterator["Coord"]:
        yield self.__class__(self.r - 1, self.c - 1)
        yield self.__class__(self.r + 0, self.c - 1)
        yield self.__class__(self.r + 1, self.c - 1)
        yield self.__class__(self.r - 1, self.c + 0)
        yield self.__class__(self.r + 1, self.c + 0)
        yield self.__class__(self.r - 1, self.c + 1)
        yield self.__class__(self.r + 0, self.c + 1)
        yield self.__class__(self.r + 1, self.c + 1)


class PartNumber(NamedTuple):
    value: int
    locs: tuple[Coord, ...]


RE_NUMBER = re.compile(r"([\d]+)")
RE_SYMBOL = re.compile(r"([^\d.])")

PartNumberLog = dict[Coord, PartNumber]
SymbolLog = dict[Coord, str]


def parse_input(input_: str) -> tuple[PartNumberLog, SymbolLog]:
    part_numbers: PartNumberLog = {}
    symbols: SymbolLog = {}

    for row_no, line in enumerate(input_.splitlines()):
        # Find and save all numbers by their occupied positions

        for m in RE_NUMBER.finditer(line.strip()):
            c_start = m.start(0)
            c_end = m.end(0)
            value = int(m.group(0))

            part_no = PartNumber(
                value,
                tuple(Coord(row_no, col_no) for col_no in range(c_start, c_end)),
            )

            for pos in part_no.locs:
                part_numbers[pos] = part_no

        # Find and save all symbols by their position
        for m in RE_SYMBOL.finditer(line.strip()):
            symbol_pos = Coord(row_no, m.start(0))
            symbols[symbol_pos] = m.group(0)

    return part_numbers, symbols


def part_a_solution(input_: str) -> Optional[int]:
    """Compute the solution to a Part A input."""
    assert len(input_) > 0

    part_numbers, symbols = parse_input(input_)
    valid_numbers: list[PartNumber] = []

    # For each position next to a symbol
    for symbol_pos in symbols:
        for near in symbol_pos.neighbors():
            # if that position matches a number
            if near in part_numbers:
                # Save the number
                part_no = part_numbers[near]
                valid_numbers.append(part_no)

                # and remove it from the list so we don't add it again
                for pos in part_no.locs:
                    del part_numbers[pos]

    return sum(p.value for p in valid_numbers)


def part_b_solution(input_: str) -> Optional[int]:
    """Compute the solution to a Part B input."""
    assert len(input_) > 0

    part_numbers, symbols = parse_input(input_)
    ratio_sum = 0

    # For each gear
    for s_pos, s in symbols.items():
        if s != "*":
            continue

        # Get unique, adjacent, part numbers
        neighbors = {
            part_numbers[n_pos] for n_pos in s_pos.neighbors() if n_pos in part_numbers
        }

        if len(neighbors) != 2:  # noqa: PLR2004
            continue

        a, b = list(neighbors)

        ratio = a.value * b.value
        ratio_sum += ratio

    return ratio_sum
