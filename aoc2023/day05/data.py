"""AOC 2023 Day 5 example data and input functions."""

from aoc2023.data import Example, get_puzzle_input

# Adding examples to a part's list signals to the system that the part is
# ready for testing

PART_A_EXAMPLES: list[Example] = [
    Example(
        """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""",
        35,
    ),
]

PART_B_EXAMPLES: list[Example] = []

PUZZLE_INPUT = get_puzzle_input(5)

PUZZLE_ANSWER_A: int | None = 346433842
PUZZLE_ANSWER_B: int | None = None
