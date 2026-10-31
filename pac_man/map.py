try:
    from .config import config
except ImportError:  # Running main.py directly from the pac_man directory.
    from config import config
import cv2

class Map:
    def __init__(self):
        self.wall_h = [[False for j in range(config.map_size[1] + 1)]
                        for i in range(config.map_size[0])]
        self.wall_v = [[False for j in range(config.map_size[1])]
                        for i in range(config.map_size[0] + 1)]
        for i in range(config.map_size[0]):
            self.wall_h[i][0] = True
            self.wall_h[i][config.map_size[1]] = True
        for j in range(config.map_size[1]):
            self.wall_v[0][j] = True
            self.wall_v[config.map_size[0]][j] = True
        
        for w in config.map_config.wall_h_list:
            for i in range(w[0], w[1]):
                try:
                    self.wall_h[i][w[2]] = True
                except:
                    pass
        for w in config.map_config.wall_v_list:
            for i in range(w[1], w[2]):
                try:
                    self.wall_v[w[0]][i] = True
                except:
                    pass
        

    def on_render(self, frame):
        for i in range(config.map_size[0]):
            for j in range(config.map_size[1] + 1):
                if(self.wall_h[i][j]):
                    cv2.line(frame, 
                             (i * config.tile_size, j * config.tile_size - 1),
                             ((i+ 1) * config.tile_size, j * config.tile_size - 1),
                             config.map_config.wall_color, 3)
        for i in range(config.map_size[0] + 1):
            for j in range(config.map_size[1]):
                if(self.wall_v[i][j]):
                    cv2.line(frame, 
                             (i * config.tile_size - 1, j * config.tile_size),
                             (i * config.tile_size - 1, (j + 1) * config.tile_size),
                             config.map_config.wall_color, 3)

    def check_wall(self, position, target):
        """Return True when the edge between two neighbouring cells is blocked."""
        if(position[0] == target[0] and position[1] == target[1]):
            return True
        elif(position[0] == target[0] and position[1] != target[1]):
            if(position[1] < target[1]):
                return self.wall_h[position[0]][target[1]]
            else:
                return self.wall_h[position[0]][position[1]]
        elif(position[0] != target[0] and position[1] == target[1]):
            if(position[0] < target[0]):
                return self.wall_v[target[0]][position[1]]
            else:
                return self.wall_v[position[0]][position[1]]
        return True

    def in_bounds(self, position):
        return (0 <= position[0] < config.map_size[0] and
                0 <= position[1] < config.map_size[1])

    def can_move(self, position, target):
        """Return True when a one-cell move is legal."""
        if not self.in_bounds(position) or not self.in_bounds(target):
            return False
        if abs(position[0] - target[0]) + abs(position[1] - target[1]) != 1:
            return False
        return not self.check_wall(position, target)

    def neighbors(self, position):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        return tuple(
            target for dx, dy in directions
            for target in [(position[0] + dx, position[1] + dy)]
            if self.can_move(position, target)
        )

    def walkable_positions(self):
        """All cells inside the board, exposed as an immutable snapshot source."""
        return frozenset(
            (x, y)
            for x in range(config.map_size[0])
            for y in range(config.map_size[1])
        )
    
map = Map()
