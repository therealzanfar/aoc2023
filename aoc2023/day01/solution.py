"""AOC 2023 Day 1 solutions."""

from typing import Optional

NUMBERS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def part_a_solution(input_: str) -> Optional[int]:
    """Compute the solution to a Part A input."""
    assert len(input_) > 0

    total = 0
    for line in input_.splitlines():
        if len(line) <= 0:
            continue

        digits = [c for c in line.strip().lower() if c.isdigit()]
        calibration = digits[0] + digits[-1]
        value = int(calibration)

        total += value

    return total


def part_b_solution(input_: str) -> Optional[int]:
    """Compute the solution to a Part B input."""
    assert len(input_) > 0

    total = 0
    for line in input_.splitlines():
        if len(line) <= 0:
            continue

        trans = convert_numbers(line)

        digits = [c for c in trans.strip().lower() if c.isdigit()]
        calibration = digits[0] + digits[-1]
        value = int(calibration)

        total += value

    return total


def convert_numbers(line: str) -> str:
    """Convert spelled-out numbers into digits."""
    parts: list[str] = []

    for x in range(len(line)):
        found = False
        for name, value in NUMBERS.items():
            if line[x:].startswith(name):
                parts.append(str(value))
                found = True
                break

        if found:
            continue

        parts.append(line[x])

    return "".join(parts)
