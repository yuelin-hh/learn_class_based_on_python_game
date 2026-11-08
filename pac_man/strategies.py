"""Reference brains for the automatic Pac-Man versus ghost battle."""

try:
    from .pathfinding import AStarPathfinder, direction_between
except ImportError:  # Running main.py directly from the pac_man directory.
    from pathfinding import AStarPathfinder, direction_between


DEFAULT_GHOST_MOVE_EVERY = 2


def predict_ghost_move(state, pathfinder, ghost, ghost_index=0, move_every=2):
    """Predict the reference ghost's next position for this turn."""
    if state.turn % max(1, move_every):
        return ghost
    direction = pathfinder.next_direction(
        ghost,
        state.pacman_position,
    )
    return direction.move(ghost) if direction is not None else ghost


class AStarGhostBrain:
    """Ghost that uses A* to chase Pac-Man through the maze.

    The ghost moves once every two turns, leaving the player a fair chance to
    react. Every time it moves, the direction still comes from a fresh A* path.
    """

    def __init__(self, move_every=DEFAULT_GHOST_MOVE_EVERY):
        self.move_every = max(1, move_every)

    def decide(self, state, ghost_index=0):
        if state.turn % self.move_every:
            return None
        start = state.ghost_positions[ghost_index]
        return AStarPathfinder(state).next_direction(
            start,
            state.pacman_position,
        )


# The name used by the original demo remains valid.
ChaseGhostBrain = AStarGhostBrain


class AutoPacManBrain:
    """Collect every bean while predicting and avoiding the chasing ghosts."""

    def __init__(self, ghost_move_every=DEFAULT_GHOST_MOVE_EVERY):
        self.target = None
        self.ghost_move_every = max(1, ghost_move_every)

    def decide(self, state):
        pathfinder = AStarPathfinder(state)
        beans = set(state.bean_positions)
        if not beans:
            return None

        pacman = state.pacman_position
        ghosts = tuple(state.ghost_positions)
        ghost_targets = tuple(
            predict_ghost_move(
                state,
                pathfinder,
                ghost,
                ghost_index=index,
                move_every=self.ghost_move_every,
            )
            for index, ghost in enumerate(ghosts)
        )
        ghost_maps = [
            pathfinder.graph_distances(ghost_target)
            for ghost_target in ghost_targets
        ]

        # Keep one target until it is eaten. Re-picking the closest bean every
        # turn can make Pac-Man pace between two equally distant cells.
        if self.target not in beans:
            pacman_distances = pathfinder.graph_distances(pacman)
            self.target = min(
                beans,
                key=lambda current_bean: pacman_distances.get(
                    current_bean,
                    float("inf"),
                ),
            )
        target_distances = pathfinder.graph_distances(self.target)

        actions = []
        for direction, target in [
            (None, pacman),
            *state.neighbors(pacman),
        ]:
            if target in ghost_targets:
                continue
            # Entering a ghost's old cell while it enters Pac-Man's old cell
            # is still a collision, even though the two cells are different.
            if any(
                target == ghost and ghost_target == pacman
                for ghost, ghost_target in zip(ghosts, ghost_targets)
            ):
                continue
            if direction is None and target not in beans:
                continue
            actions.append((direction, target))

        if not actions:
            return None

        def score(action):
            direction, target = action
            target_distance = target_distances.get(target, 999)
            safety = min(
                (
                    ghost_map.get(target, 999)
                    for ghost_map in ghost_maps
                ),
                default=999,
            )
            exits = sum(
                1
                for _, neighbour in state.neighbors(target)
                if neighbour not in ghost_targets
            )
            return (
                -target_distance * 20
                + min(safety, 6) * 12
                + exits * 2
                + (20 if target in beans else 0)
            )

        return max(actions, key=score)[0]


class GreedyPacManBrain(AutoPacManBrain):
    """Backwards-compatible name for the automatic Pac-Man."""
