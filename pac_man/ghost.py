import cv2

try:
    from .config import config
    from .interfaces import Direction
    from .map import map
except ImportError:  # Running main.py directly from the pac_man directory.
    from config import config
    from interfaces import Direction
    from map import map


class Ghost:
    def __init__(self, position, color=(255, 80, 80)):
        self.position = tuple(position)
        self.color = color

    def move(self, direction):
        if not isinstance(direction, Direction):
            return False
        target = direction.move(self.position)
        if not map.can_move(self.position, target):
            return False
        self.position = target
        return True

    def on_render(self, frame):
        center = (
            int((self.position[0] + 0.5) * config.tile_size),
            int((self.position[1] + 0.5) * config.tile_size),
        )
        cv2.circle(frame, center, config.ghost_config.radious, self.color, -1, cv2.LINE_AA)
        cv2.circle(frame, (center[0] - 6, center[1] - 3), 3, (255, 255, 255), -1)
        cv2.circle(frame, (center[0] + 6, center[1] - 3), 3, (255, 255, 255), -1)

