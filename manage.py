#! /usr/bin/env python3

"""Management script for aoc2023."""

import logging
import os
import sys
from pathlib import Path
from typing import Any

import aocd  # type: ignore[import-untyped]
import click
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from rich.logging import RichHandler

import aoc2023
from aoc2023.data import (
    DAY_COUNT_MAX,
    DAY_COUNT_MIN,
    DAY_SUBMODULE_FMT,
    PUZZLE_INPUT_FILENAME,
    YEAR,
)

CLICK_CONTEXT = {"help_option_names": ["-h", "--help"]}
DAY_TEMPLATE_PATH = Path(__file__).absolute().parent / "templates" / "day"


def setup_logging(verbosity: int = 0) -> None:
    """
    Set up a root logger with console output.

    Args:
        verbosity (int, optional): The logging level; 0=Error, 1=Warning,
            2=Info, 3+=Debug. Defaults to 0.
    """
    logging_level = logging.ERROR
    if verbosity == 1:
        logging_level = logging.WARNING
    elif verbosity == 2:  # noqa: PLR2004
        logging_level = logging.INFO
    elif verbosity >= 3:  # noqa: PLR2004
        logging_level = logging.DEBUG

    logging.basicConfig(
        level=logging_level,
        format="%(message)s",
        datefmt="[%x]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )


def get_day_path(day: int) -> Path:
    """Return the path to the particular day's submodule."""
    return Path(
        aoc2023.__file__,
    ).absolute().parent / DAY_SUBMODULE_FMT.format(day)


def get_puzzle_input_path(day: int) -> Path:
    """Return the path to the particular day's input."""
    return get_day_path(day) / PUZZLE_INPUT_FILENAME


def _get_puzzle_input(year: int, day: int) -> str:
    """Extract the personalized puzzle input from the AoC website."""
    logger = logging.getLogger(__name__)

    load_dotenv()
    aoc_token = os.getenv("AOC_SESSION", None)
    if aoc_token is None:
        logger.warning("No AoC token found")
        return ""

    try:
        u = aocd.models.User(token=aoc_token)
        p = aocd.models.Puzzle(year=year, day=day, user=u)
        return p.input_data

    except Exception:  # If anything fails, we still want to write the file
        logger.warning("advent-of-code-data could not load the puzzle input")
        return ""


@click.group(context_settings=CLICK_CONTEXT)
@click.option("-v", "--verbose", count=True)
def manage(verbose: int = 0) -> int:
    """Manage the AOC Package."""
    args = locals().items()
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    logger.debug(
        "Running with options: %s",
        ", ".join(f"{k!s}={v!r}" for k, v in args),
    )

    return 0


@click.command()
@click.argument("number", type=int)
def create_new_day(number: int) -> None:
    """
    Create a new submodule for a day's solutions.

    NUMBER is the day number to create the submodule for
    """
    logger = logging.getLogger(__name__)

    if number < DAY_COUNT_MIN or number > DAY_COUNT_MAX:
        raise click.ClickException("{number} is an invalid day number")

    day_path = get_day_path(number)

    if day_path.exists() and len(list(day_path.iterdir())) > 0:
        raise click.ClickException("Day {number} already exists")

    day_jinja_env = Environment(
        loader=FileSystemLoader(DAY_TEMPLATE_PATH, encoding="utf-8"),
        keep_trailing_newline=True,
    )

    logger.info("Creating new day submodule at %s", day_path)

    if not day_path.exists():
        logger.debug("Creating submodule directory")
        day_path.mkdir(exist_ok=True)

    puzzle_input_path = get_puzzle_input_path(day=number)
    puzzle_input = _get_puzzle_input(YEAR, number)

    if not puzzle_input:
        logger.warning(
            "Puzzle input will be generated without data. "
            "Manually save puzzle input to %s",
            puzzle_input_path,
        )
    else:
        logger.info("Saving Puzzle input to %s", puzzle_input_path)

    puzzle_input_path.write_text(puzzle_input)

    # Part B solutions aren't available publicly, or privately until Part A
    # has been solved, so we will leave extraction up to the user.
    template_context: dict[str, Any] = {
        "aoc_year": YEAR,
        "day_number": number,
        "day_path": day_path,
        "day_module": DAY_SUBMODULE_FMT.format(number),
        "sample_a_input": "",
        "sample_b_input": "",
        "sample_a_solution": "",
        "sample_b_solution": "",
    }
    logger.debug("Rendering templates using context: %s", repr(template_context))

    for template_filename in day_jinja_env.list_templates():
        if template_filename.endswith(".j2"):
            output_filename = Path(template_filename).stem
            logger.info(
                "- Rendering %s template as %s",
                template_filename,
                output_filename,
            )
            template = day_jinja_env.get_template(template_filename)

            with open(day_path / output_filename, "w", encoding="utf-8") as out_fh:
                out_fh.write(template.render(**template_context))


manage.add_command(create_new_day, name="create")


if __name__ == "__main__":
    sys.exit(manage())
