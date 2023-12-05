"""AOC 2023 Day 5 solutions."""

import logging
import re
from dataclasses import dataclass, field
from typing import NamedTuple, Optional

RE_MAP_START = re.compile(r"(?P<src>[a-z]+)-to-(?P<dst>[a-z]+) map:")


class Range(NamedTuple):
    src_start: int
    dst_start: int
    size: int

    def contains(self, value: int) -> bool:
        return value >= self.src_start and value < self.src_start + self.size

    def convert(self, value: int) -> int:
        return value - self.src_start + self.dst_start


class Item(NamedTuple):
    name: str
    value: int


@dataclass
class Map:
    dst: str
    ranges: list[Range] = field(default_factory=list)

    def convert(self, value: int) -> Item:
        for r in self.ranges:
            if r.contains(value):
                return Item(self.dst, r.convert(value))

        # If no range is found
        return Item(self.dst, value)


@dataclass
class Data:
    sources: list[Item] = field(default_factory=list)
    maps: dict[str, Map] = field(default_factory=dict)

    def convert(self, item: Item) -> Item:
        logger = logging.getLogger(__name__)

        if item.name not in self.maps:
            raise ValueError(f"No {item.name} Map found")

        mapped = self.maps[item.name].convert(item.value)

        logger.debug(f"{item} -> {mapped}")

        return mapped

    @classmethod
    def parse(cls, input_: str) -> "Data":
        data = cls()

        source_state = True
        current_map = ""

        for line in input_.splitlines():
            if len(line) <= 0:
                continue

            if source_state:
                name, ids = line.split(":")

                if name.endswith("s"):
                    name = name[:-1]

                data.sources = [Item(name, int(id_.strip())) for id_ in ids.split()]
                source_state = False

            elif m := RE_MAP_START.match(line):
                current_map = m.group("src")
                data.maps[current_map] = Map(
                    m.group("dst"),
                )

            else:
                dst, src, size = line.split()
                data.maps[current_map].ranges.append(
                    Range(int(src), int(dst), int(size)),
                )

        return data


def part_a_solution(input_: str) -> Optional[int]:
    """Compute the solution to a Part A input."""
    assert len(input_) > 0

    d = Data.parse(input_)

    locations: list[int] = []

    for i in d.sources:
        item = i
        while item.name != "location":
            item = d.convert(item)
        locations.append(item.value)

    return min(locations)


def part_b_solution(input_: str) -> Optional[int]:
    """Compute the solution to a Part B input."""
    assert len(input_) > 0
    return None
