"""AOC 2023 Day 4 example tests."""

import pytest

from aoc2023.day04.data import PART_A_EXAMPLES, PART_B_EXAMPLES
from aoc2023.day04.solution import part_a_solution, part_b_solution


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        pytest.param(example.input, example.solution, id=f"{seq:02d}")
        for seq, example in enumerate(PART_A_EXAMPLES)
    ],
)
def test_example_a(given: str, expected: int) -> None:
    """Test the part a solution on the given example."""
    assert part_a_solution(given) == expected


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        pytest.param(example.input, example.solution, id=f"{seq:02d}")
        for seq, example in enumerate(PART_B_EXAMPLES)
    ],
)
def test_example_b(given: str, expected: int) -> None:
    """Test the part a solution on the given example."""
    assert part_b_solution(given) == expected
