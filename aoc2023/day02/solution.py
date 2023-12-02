"""AOC 2023 Day 2 solutions."""

from typing import Optional


def part_a_solution(input_: str) -> Optional[int]:
    """Compute the solution to a Part A input."""
    assert len(input_) > 0

    maximums = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    possible_count = 0

    for gamedef in input_.splitlines():
        gameid, info = gamedef.split(":")
        possible = True

        for event in info.split(";"):
            colors = [s.strip() for s in event.split(",")]
            for color in colors:
                num, name = color.split(" ")
                if int(num) > maximums[name]:
                    possible = False
                    break

                if not possible:
                    break

            if not possible:
                break

        if not possible:
            continue

        game_num = int(gameid[5:])
        possible_count += game_num

    return possible_count


def part_b_solution(input_: str) -> Optional[int]:
    """Compute the solution to a Part B input."""
    assert len(input_) > 0

    total_power = 0

    for gamedef in input_.splitlines():
        _, info = gamedef.split(":")

        minimums = {
            "blue": 0,
            "green": 0,
            "red": 0,
        }

        for event in info.split(";"):
            colors = [s.strip() for s in event.split(",")]
            for color in colors:
                num, name = color.split(" ")

                if int(num) > minimums[name]:
                    minimums[name] = int(num)

        power = minimums["blue"] * minimums["green"] * minimums["red"]
        total_power += power

    return total_power
