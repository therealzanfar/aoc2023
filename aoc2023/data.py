"""Generic puzzle input code."""

import importlib.resources
import importlib.util
import logging
from typing import Callable, NamedTuple, Optional

import aoc2023

YEAR = 2023

DAY_COUNT_MIN = 1
DAY_COUNT_MAX = 25
DAY_SUBMODULE_FMT = "day{:02d}"

PART_NAMES = ("A", "B")

PUZZLE_INPUT_FILENAME = "input.data"


class Example(NamedTuple):
    """Puzzle solution example."""

    input: str  # noqa: A003
    solution: Optional[int]


def get_puzzle_input(day: int) -> str:
    """Extract that day's input and return it as a string."""
    puzzle_input_path = (
        importlib.resources.files(
            getattr(aoc2023, DAY_SUBMODULE_FMT.format(day)),
        )
        / PUZZLE_INPUT_FILENAME
    )

    with puzzle_input_path.open("rt", encoding="utf-8") as input_fh:
        return input_fh.read().strip()


def days_with_solutions() -> list[int]:
    """Identify which days have solutions."""
    logger = logging.getLogger(__name__)
    days: list[int] = []

    for d in range(DAY_COUNT_MIN, DAY_COUNT_MAX + 1):
        m = DAY_SUBMODULE_FMT.format(d)
        if importlib.util.find_spec(f"aoc{YEAR}.{m}"):
            days.append(d)

    logger.debug("Available days: %s", days)
    return days


def day_parts_with_solutions(day: int) -> list[str]:
    """Identify which parts of a day have solutions."""
    logger = logging.getLogger(__name__)
    parts: list[str] = []

    # PART_A_EXAMPLES
    dm = DAY_SUBMODULE_FMT.format(day)
    sm = f"aoc{YEAR}.{dm}.data"

    try:
        importlib.import_module(sm)
    except ImportError:
        logger.debug("Could not import day %s submodule %s", day, sm)
        return []

    data_module = getattr(globals()[f"aoc{YEAR}"], dm).data

    for p in PART_NAMES:
        part_examples_name = f"PART_{p.upper()}_EXAMPLES"
        if hasattr(data_module, part_examples_name):
            examples = getattr(data_module, part_examples_name)
            if len(examples) > 0:
                parts.append(p)
                continue

            logger.debug("Day %s, Part %s has no examples", day, p)
            break

        logger.debug(
            "Day %s data submodule has no variable named %s",
            day,
            part_examples_name,
        )
        break

    logger.debug("Available parts: %s", parts)
    return parts


def get_puzzle_solution(
    day: int,
    part: str,
) -> Callable[[str], int]:
    """Return the solution method for the specified day and part."""
    dm = DAY_SUBMODULE_FMT.format(day)
    sm = f"aoc{YEAR}.{dm}.solution"
    fn = f"part_{part.lower()}_solution"

    importlib.import_module(sm)
    solutions_module = getattr(globals()[f"aoc{YEAR}"], dm).solution

    return getattr(solutions_module, fn)


def get_puzzle_inputs(day: int, part: str, test: bool = False) -> list[Example]:
    """Return the input for the specified day and part."""
    dm = DAY_SUBMODULE_FMT.format(day)
    sm = f"aoc{YEAR}.{dm}.data"

    importlib.import_module(sm)
    data_module = getattr(globals()[f"aoc{YEAR}"], dm).data

    if test:
        part_examples_name = f"PART_{part.upper()}_EXAMPLES"
        return getattr(data_module, part_examples_name)

    return [
        Example(data_module.PUZZLE_INPUT, None),
    ]
