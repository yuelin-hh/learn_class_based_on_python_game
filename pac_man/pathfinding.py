"""Reusable graph search built on the read-only battle state."""

import heapq
from collections import deque
from itertools import count

try:
    from .interfaces import Direction
except ImportError:  # Running main.py directly from the pac_man directory.
    from interfaces import Direction


def direction_between(start, target):
    """Return the direction of a one-cell move, or None for a non-move."""
    delta = (target[0] - start[0], target[1] - start[1])
    for direction in Direction:
        if direction.delta == delta:
            return direction
    return None


class AStarPathfinder:
    """A* search over the cells in a ``BattleState`` snapshot."""

    def __init__(self, state):
        self.state = state

    @staticmethod
    def heuristic(first, second):
        # Manhattan distance never overestimates a four-direction grid path.
        return abs(first[0] - second[0]) + abs(first[1] - second[1])

    def shortest_path(self, start, goal, blocked=frozenset()):
        """Return the shortest path as a tuple, including both endpoints."""
        start = tuple(start)
        goal = tuple(goal)
        blocked = set(blocked)
        if start == goal:
            return (start,)
        if goal in blocked or goal not in self.state.walkable_positions:
            return ()

        sequence = count()
        frontier = [
            (self.heuristic(start, goal), 0, next(sequence), start)
        ]
        cost_so_far = {start: 0}
        parent = {start: None}

        while frontier:
            _, cost, _, position = heapq.heappop(frontier)
            if position == goal:
                path = []
                while position is not None:
                    path.append(position)
                    position = parent[position]
                return tuple(reversed(path))

            if cost != cost_so_far.get(position):
                continue

            for _, target in self.state.neighbors(position):
                if target in blocked:
                    continue
                new_cost = cost + 1
                if new_cost >= cost_so_far.get(target, float("inf")):
                    continue
                cost_so_far[target] = new_cost
                parent[target] = position
                priority = new_cost + self.heuristic(target, goal)
                heapq.heappush(
                    frontier,
                    (priority, new_cost, next(sequence), target),
                )
        return ()

    def next_direction(self, start, goal, blocked=frozenset()):
        """Return the first direction on the A* path to ``goal``."""
        path = self.shortest_path(start, goal, blocked)
        if len(path) < 2:
            return None
        return direction_between(path[0], path[1])

    def graph_distances(self, start, blocked=frozenset()):
        """Return shortest-path distances from ``start`` to every reachable cell."""
        blocked = set(blocked)
        if start in blocked:
            return {}
        distances = {start: 0}
        queue = deque([start])
        while queue:
            position = queue.popleft()
            for _, target in self.state.neighbors(position):
                if target in blocked or target in distances:
                    continue
                distances[target] = distances[position] + 1
                queue.append(target)
        return distances
