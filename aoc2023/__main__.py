#! /usr/bin/env python3

"""Console script for aoc2023."""

import logging
import sys

import click
from rich.console import Console
from rich.logging import RichHandler

from aoc2023.data import (
    DAY_COUNT_MAX,
    DAY_COUNT_MIN,
    PART_NAMES,
    YEAR,
    day_parts_with_solutions,
    days_with_solutions,
    get_puzzle_inputs,
    get_puzzle_solution,
)

CLICK_CONTEXT = {"help_option_names": ["-h", "--help"]}

ANSWER_FORMAT = "7d"


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


@click.command(context_settings=CLICK_CONTEXT)
@click.argument("DAY", required=False, default="")
@click.argument("PART", required=False, default="")
@click.option(
    "--test",
    "-t",
    is_flag=True,
    flag_value=True,
    default=False,
    type=bool,
    help="Processes the example inputs instead of the user input",
)
@click.option("-v", "--verbose", count=True)
def cli(  # noqa: C901, PLR0912
    day: str = "",
    part: str = "",
    test: bool = False,
    verbose: int = 0,
) -> int:
    """
    Compute the solution for a given day's problem.

    DAY (1-25) and PART (A, B) select which problem to compute the solution
    to. If omitted, the system will attempt to identify the most recent,
    finished solution and compute that.
    """
    args = locals().items()
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    logger.debug(
        "Running with options: %s",
        ", ".join(f"{k!s}={v!r}" for k, v in args),
    )

    available_days = days_with_solutions()
    if len(available_days) < 1:
        raise click.ClickException("No days have solutions to compute")

    if day == "":
        day = str(available_days[-1])
        logger.info("Choosing most recent day, %s", day)

    try:
        day_no = int(day)
    except ValueError as e:
        raise click.ClickException(f"Invalid DAY selection: {day}") from e

    if day_no < DAY_COUNT_MIN or day_no > DAY_COUNT_MAX:
        raise click.ClickException(f"Invalid DAY value: {day_no}")

    available_parts = day_parts_with_solutions(day_no)
    if len(available_parts) < 1:
        raise click.ClickException(f"Day {day_no} has no solutions to compute")

    part = part.upper()
    if part == "":
        part = available_parts[-1].upper()
        logger.info("Choosing day %s most recent part, %s", day, part)

    if part not in PART_NAMES:
        raise click.ClickException(f"Invalid PART selection: {part}")

    data = get_puzzle_inputs(day_no, part, test)
    solution = get_puzzle_solution(day_no, part)

    c = Console(highlight=False)
    rprint = c.print

    for _idx, example in enumerate(data):
        answer = solution(example.input) or 0
        rprint(
            rf"Year [blue]{YEAR}[/blue], "
            rf"Day [blue]{day_no:02d}[/blue], "
            rf"Part [blue]{part.upper()}[/blue]: "
            rf"Solution=[bright_white]{answer:{ANSWER_FORMAT}}[/bright_white], ",
            end="",
        )

        expected = example.solution
        if expected is not None:
            rprint(
                rf"Expected=[bright_white]{expected:{ANSWER_FORMAT}}[/bright_white]",
                end="",
            )

            if answer == expected:
                rprint(r"   [green]\[CORRECT][/green]")
            else:
                rprint(r"   [red]\[WRONG][/red]")

        else:
            print()

    return 0


if __name__ == "__main__":
    sys.exit(cli())
