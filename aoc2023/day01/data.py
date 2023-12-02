"""AOC 2023 Day 1 example data and input functions."""

from aoc2023.data import Example, get_puzzle_input

# Adding examples to a part's list signals to the system that the part is
# ready for testing

PART_A_EXAMPLES: list[Example] = [
    Example(
        """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
""",
        142,
    ),
]

PART_B_EXAMPLES: list[Example] = [
    Example(
        """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
""",
        281,
    ),
]

PUZZLE_INPUT = get_puzzle_input(1)

PUZZLE_ANSWER_A: int | None = 56465
PUZZLE_ANSWER_B: int | None = 55902
