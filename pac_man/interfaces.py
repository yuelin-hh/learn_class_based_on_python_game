"""The small, stable API used by the Pac-Man classroom battle.

Students only need to implement ``decide`` on one of the two brain classes.
The game never gives a brain a mutable game object; every call receives a
read-only snapshot instead.
"""

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Protocol, Tuple

Position = Tuple[int, int]


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3
    # Backwards-compatible names used by the original lesson code.
    Right = RIGHT
    Down = DOWN
    Left = LEFT
    Up = UP

    @property
    def delta(self) -> Position:
        return ((1, 0), (0, 1), (-1, 0), (0, -1))[self.value]

    @property
    def heading(self) -> int:
        return self.value

    def move(self, position: Position) -> Position:
        dx, dy = self.delta
        return position[0] + dx, position[1] + dy

    @classmethod
    def from_key(cls, key: int):
        return {
            ord("d"): cls.RIGHT,
            ord("s"): cls.DOWN,
            ord("a"): cls.LEFT,
            ord("w"): cls.UP,
        }.get(key)


@dataclass(frozen=True)
class BattleState:
    """Immutable information visible to a strategy for one turn."""

    turn: int
    map_size: Position
    pacman_position: Position
    ghost_positions: Tuple[Position, ...]
    bean_positions: FrozenSet[Position]
    # These are immutable snapshots so a strategy cannot mutate game state.
    walkable_positions: FrozenSet[Position]
    legal_moves: FrozenSet[Tuple[Position, Position]] = frozenset()

    def can_move(self, position: Position, direction: Direction) -> bool:
        target = direction.move(position)
        if self.legal_moves:
            return (position, target) in self.legal_moves
        return target in self.walkable_positions

    def neighbors(self, position: Position) -> Tuple[Tuple[Direction, Position], ...]:
        return tuple(
            (direction, direction.move(position))
            for direction in Direction
            if self.can_move(position, direction)
        )


class PacManBrain(Protocol):
    def decide(self, state: BattleState) -> Direction:
        """Return the next direction, or ``None`` to stay still."""


class GhostBrain(Protocol):
    def decide(self, state: BattleState, ghost_index: int = 0) -> Direction:
        """Return the next direction for one ghost, or ``None`` to wait."""


def call_brain(brain, state: BattleState, ghost_index: int = 0):
    """Call both the simple function form and the class form of a brain."""
    if brain is None:
        return None
    if hasattr(brain, "decide"):
        if ghost_index is None:
            return brain.decide(state)
        try:
            return brain.decide(state, ghost_index)
        except TypeError:
            return brain.decide(state)
    if ghost_index is None:
        return brain(state)
    try:
        return brain(state, ghost_index)
    except TypeError:
        return brain(state)

