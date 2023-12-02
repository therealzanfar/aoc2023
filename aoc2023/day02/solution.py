"""AOC 2023 Day 2 solutions."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RoundTotal:  # noqa: D101
    r: int = 0
    g: int = 0
    b: int = 0


@dataclass
class Round:  # noqa: D101
    r: int | None = None
    g: int | None = None
    b: int | None = None

    @classmethod
    def parse(cls, line: str) -> "Round":  # noqa: D102
        data: dict[str, int] = {}
        colors = [s.strip() for s in line.split(",")]
        for color in colors:
            num, name = color.split(" ")

            data[name.strip().lower()[0]] = int(num.strip())

        return cls(**data)


@dataclass
class Game:  # noqa: D101
    id_: int
    rounds: list[Round] = field(default_factory=list)

    @classmethod
    def parse(cls, line: str) -> "Game":  # noqa: D102
        game, info = line.split(":")
        game_id = int(game.strip()[5:])
        rounds = tuple(e.strip() for e in info.split(";"))

        return cls(
            game_id,
            [Round.parse(r) for r in rounds],
        )

    @property
    def maximums(self) -> RoundTotal:  # noqa: D102
        return RoundTotal(
            **{
                color: max(getattr(rnd, color) or 0 for rnd in self.rounds)
                for color in ("r", "g", "b")
            },
        )


def part_a_solution(input_: str) -> Optional[int]:
    """Compute the solution to a Part A input."""
    assert len(input_) > 0

    maximums = RoundTotal(
        12,
        13,
        14,
    )

    possible_total = 0
    games = [Game.parse(line) for line in input_.splitlines()]
    for g in games:
        maxes = g.maximums

        if maxes.r <= maximums.r and maxes.g <= maximums.g and maxes.b <= maximums.b:
            possible_total += g.id_

    return possible_total


def part_b_solution(input_: str) -> Optional[int]:
    """Compute the solution to a Part B input."""
    assert len(input_) > 0

    total_power = 0
    games = [Game.parse(line) for line in input_.splitlines()]

    for g in games:
        m = g.maximums
        power = m.r * m.g * m.b
        total_power += power

    return total_power
