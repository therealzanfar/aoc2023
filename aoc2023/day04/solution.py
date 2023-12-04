"""AOC 2023 Day 4 solutions."""

from typing import NamedTuple, Optional


class Card(NamedTuple):
    id_: int
    winning: set[int]
    present: set[int]

    @classmethod
    def parse(cls, line: str) -> "Card":
        name, numbers = line.strip().split(":")
        card_no = int(name[5:])

        win, pres = numbers.strip().split("|")

        return cls(
            card_no,
            {int(n.strip()) for n in win.split(" ") if n != ""},
            {int(n.strip()) for n in pres.split(" ") if n != ""},
        )

    @property
    def winning_numbers(self) -> set[int]:
        return self.present & self.winning

    @property
    def winning_score(self) -> int:
        count = len(self.winning_numbers)
        if count <= 0:
            return 0

        return 2 ** (count - 1)


def part_a_solution(input_: str) -> Optional[int]:
    """Compute the solution to a Part A input."""
    assert len(input_) > 0

    return sum(Card.parse(line).winning_score for line in input_.splitlines())


def part_b_solution(input_: str) -> Optional[int]:
    """Compute the solution to a Part B input."""
    assert len(input_) > 0

    cards = [Card.parse(line) for line in input_.splitlines()]
    count = [1 for _ in cards]

    for idx, card in enumerate(cards):
        new_cards = len(card.winning_numbers)
        copies = count[idx]

        for copy in range(idx + 1, idx + new_cards + 1):
            if copy < len(cards):
                count[copy] += copies

    return sum(count)
