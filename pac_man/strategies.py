"""Small reference strategies used by the demo and useful as student examples."""

from collections import deque

try:
    from .interfaces import Direction
except ImportError:  # Running main.py directly from the pac_man directory.
    from interfaces import Direction


def _first_step(state, start, goals, forbidden=()):
    goals = set(goals)
    if not goals:
        return None
    blocked = set(forbidden)
    queue = deque([(start, None)])
    visited = {start}
    while queue:
        position, first_direction = queue.popleft()
        if position in goals and position != start:
            return first_direction
        for direction, target in state.neighbors(position):
            if target in visited or target in blocked:
                continue
            visited.add(target)
            queue.append((target, first_direction or direction))
    return None


class ChaseGhostBrain:
    """Breadth-first ghost: always takes the shortest route to Pac-Man."""

    def decide(self, state, ghost_index=0):
        start = state.ghost_positions[ghost_index]
        return _first_step(state, start, [state.pacman_position])


class GreedyPacManBrain:
    """Collect beans with BFS while avoiding a ghost on the next cell."""

    def decide(self, state):
        danger = set(state.ghost_positions)
        safe_beans = [bean for bean in state.bean_positions if bean not in danger]
        direction = _first_step(state, state.pacman_position, safe_beans, danger)
        if direction is not None:
            return direction
        # When a ghost is close, moving to any legal non-ghost cell is better
        # than waiting in place.
        for direction, target in state.neighbors(state.pacman_position):
            if target not in danger:
                return direction
        return None

