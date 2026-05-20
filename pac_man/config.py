class PacManConfig:
    radious = 16
    position = [8, 8]
    frame_interval = 0.2
    color = (0, 240, 255)
    speed = 3

class BeanConfig:
    color = (0, 160, 160)
    color_shining = (0, 240, 255)
    frame_interval = 0.5
    radious = 2
    positions = [ 
        (3, 3)
    ]

class MapConfig:
    wall_color = (240, 240, 40)
    wall_h_list = [
        (1, 4, 1), (12, 15, 1),
        (2, 14, 2),
        (3, 6, 3), (10, 13, 3),
        (1, 3, 4), (13, 15, 4),
        (4, 6, 4), (10, 12, 4),
        (5, 11, 5),
        (4, 6, 9), (7, 9, 9), (10, 12, 9),
        (0, 3, 11), (13, 16, 11),
        (1, 2, 12), (4, 6, 12), (10, 12, 12), (14, 15, 12),
        (6, 10, 14),
        (5, 7, 15), (9, 11, 15),

    ]
    wall_v_list = [
        (8, 0, 1),
        (1, 1, 3), (15, 1, 3),
        (6, 3, 4), (10, 3, 4),
        (8, 3, 5),
        (4, 4, 8), (12, 4, 8),
        (2, 4, 10), (14, 4, 10),
        (7, 7, 9), (9, 7, 9),
        (3, 7, 11), (13, 7, 11),
        (6, 9, 12), (10, 9, 12),
        (1, 12, 15), (15, 12, 15),
        (8, 11, 14),
        (3, 14, 16), (13, 14, 16),
        (5, 13, 15), (11, 13, 15),
    ]
    
class Config:
    def __init__(self):
        self.__init_bean_position()
        pass

    def __init_bean_position(self):
        self.bean_config.positions.clear()
        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                self.bean_config.positions.append((i, j))

    pacman_config = PacManConfig()
    bean_config = BeanConfig()
    map_config = MapConfig()
    map_size = (16, 16)
    tile_size = 40
    eat_range = 0.2
    tex_color = (0, 240, 255)
    is_end = False

config = Config()