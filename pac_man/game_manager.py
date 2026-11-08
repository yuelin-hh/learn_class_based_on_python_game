import cv2
import numpy as np

try:
    from . import pac_man
    from . import bean
    from .config import config
    from .ghost import Ghost
    from .interfaces import BattleState, Direction, call_brain
    from .map import map
    from .strategies import AStarGhostBrain, AutoPacManBrain
except ImportError:  # Running main.py directly from the pac_man directory.
    import pac_man
    import bean
    from config import config
    from ghost import Ghost
    from interfaces import BattleState, Direction, call_brain
    from map import map
    from strategies import AStarGhostBrain, AutoPacManBrain


class GameManager:
    """Runs a battle while keeping strategy code outside the game engine."""

    RUNNING = "running"
    WIN = "win"
    LOSE = "lose"

    def __init__(self, pacman_brain=None, ghost_brains=None, turn_interval=0.18):
        self.pacman_brain = pacman_brain
        self.ghost_brains = list(ghost_brains or [])
        self.turn_interval = turn_interval
        self._turn_timer = 0.0
        self.reset()

    def reset(self):
        self.player = pac_man.PacMan()
        ghost_positions = config.ghost_config.positions
        colors = config.ghost_config.colors
        self.ghosts = [
            Ghost(position, colors[i % len(colors)])
            for i, position in enumerate(ghost_positions)
        ]
        self.bean_list = [bean.Bean(position) for position in config.bean_config.positions]
        self.turn = 0
        self.status = self.RUNNING
        self._turn_timer = 0.0
        self.elapsed_time = 0.0
        self.finished_time = None
        config.is_end = False

    @property
    def result(self):
        return self.status

    def on_input(self, key):
        """Keep the original keyboard mode available when no Pac-Man brain is set."""
        if self.pacman_brain is None and self.status == self.RUNNING:
            self.player.on_input(key)

    def on_update(self, delta):
        if self.status != self.RUNNING:
            return
        self.elapsed_time += max(0.0, delta)
        for current_bean in self.bean_list:
            current_bean.on_update(delta)

        if self.pacman_brain is None:
            self.player.on_update(delta)
            if self._check_collision():
                self._finish(self.LOSE)
            return

        self._turn_timer += delta
        while self._turn_timer >= self.turn_interval and self.status == self.RUNNING:
            self._turn_timer -= self.turn_interval
            self.step()

    def step(self):
        """Run exactly one simultaneous strategy turn and return the result."""
        if self.status != self.RUNNING:
            return self.status
        before_pacman = tuple(self.player.position)
        before_ghosts = tuple(ghost.position for ghost in self.ghosts)
        state = self._state()

        pacman_direction = self._direction(
            call_brain(self.pacman_brain, state, ghost_index=None)
        )
        ghost_directions = [
            self._direction(
                call_brain(self._ghost_brain(index), state, ghost_index=index)
            )
            for index in range(len(self.ghosts))
        ]

        if pacman_direction is not None:
            self.player.move(pacman_direction)
        for ghost, direction in zip(self.ghosts, ghost_directions):
            if direction is not None:
                ghost.move(direction)

        self.turn += 1
        if self._check_collision(before_pacman, before_ghosts):
            self._finish(self.LOSE)
        else:
            self._eat_beans()
            if not self.bean_list:
                self._finish(self.WIN)
        return self.status

    def _finish(self, status):
        self.status = status
        self.finished_time = self.elapsed_time
        config.is_end = True

    @property
    def elapsed_seconds(self):
        """The final time after the match, or the live time while running."""
        if self.finished_time is not None:
            return self.finished_time
        return self.elapsed_time

    def _direction(self, value):
        return value if isinstance(value, Direction) else None

    def _ghost_brain(self, index):
        if not self.ghost_brains:
            return None
        # One submitted ghost brain can control every ghost in a match.
        return self.ghost_brains[min(index, len(self.ghost_brains) - 1)]

    def _state(self):
        walkable_positions = map.walkable_positions()
        legal_moves = frozenset(
            (position, direction.move(position))
            for position in walkable_positions
            for direction in Direction
            if map.can_move(position, direction.move(position))
        )
        return BattleState(
            turn=self.turn,
            map_size=tuple(config.map_size),
            pacman_position=tuple(self.player.position),
            ghost_positions=tuple(ghost.position for ghost in self.ghosts),
            bean_positions=frozenset(tuple(current_bean.position) for current_bean in self.bean_list),
            walkable_positions=walkable_positions,
            legal_moves=legal_moves,
        )

    def _eat_beans(self):
        current_position = tuple(self.player.position)
        self.bean_list = [
            current_bean for current_bean in self.bean_list
            if tuple(current_bean.position) != current_position
        ]

    def _check_collision(self, before_pacman=None, before_ghosts=None):
        pacman_position = tuple(self.player.position)
        ghost_positions = [ghost.position for ghost in self.ghosts]
        if pacman_position in ghost_positions:
            return True
        if before_pacman is not None and before_ghosts is not None:
            for before_ghost, ghost in zip(before_ghosts, ghost_positions):
                if before_pacman == ghost and before_ghost == pacman_position:
                    return True
        return False

    def on_render(self):
        frame = self.__create_frame()
        map.on_render(frame)
        for current_bean in self.bean_list:
            current_bean.on_render(frame)
        for ghost in self.ghosts:
            ghost.on_render(frame)
        self.player.on_render(frame)
        cv2.putText(
            frame,
            "Beans: {}  Time: {:.2f}s".format(len(self.bean_list), self.elapsed_seconds),
            (10, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA,
        )
        return frame

    def __create_frame(self):
        frame = np.zeros(
            (config.map_size[1] * config.tile_size,
             config.map_size[0] * config.tile_size, 3),
            dtype=np.uint8,
        )
        for i in range(config.map_size[0]):
            cv2.line(
                frame, (i * config.tile_size, 0),
                (i * config.tile_size, config.map_size[1] * config.tile_size),
                (120, 120, 120), 1,
            )
        for i in range(config.map_size[1]):
            cv2.line(
                frame, (0, i * config.tile_size),
                (config.map_size[0] * config.tile_size, i * config.tile_size),
                (120, 120, 120), 1,
            )
        return frame

    def show_win(self):
        frame = np.zeros(
            (config.map_size[1] * config.tile_size,
             config.map_size[0] * config.tile_size, 3),
            dtype=np.uint8,
        )
        text = "You Win!" if self.status == self.WIN else "Caught!"
        cv2.putText(frame, text, (40, 280), cv2.FONT_HERSHEY_DUPLEX,
                    4, config.tex_color, 3, cv2.LINE_AA)
        cv2.putText(frame, "Time: {:.2f}s".format(self.elapsed_seconds),
                    (105, 360), cv2.FONT_HERSHEY_DUPLEX,
                    1.6, (255, 255, 255), 2, cv2.LINE_AA)
        return frame


# Students can replace these two objects in main.py without touching the engine.
gamemanager = GameManager(
    pacman_brain=AutoPacManBrain(),
    ghost_brains=[AStarGhostBrain()],
)
