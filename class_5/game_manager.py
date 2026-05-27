from config import config
from map import map
import pac_man
import bean

import cv2
import numpy as np

class GameManager:
    def __init__(self):
        self.player = pac_man.PacMan()
        self.bean_list = []
        for p in config.bean_config.positions:
            self.bean_list.append(bean.Bean(p))

    def on_input(self, key):
        self.player.on_input(key)

    def on_update(self, delta):
        self.player.on_update(delta)
        to_remove = [b for b in self.bean_list if bean.check_eat(self.player.position, b.position)]
        for b in to_remove:
            self.bean_list.remove(b)
        if (len(self.bean_list) == 0):
            config.is_end = True
            return
        for b in self.bean_list:
            b.on_update(delta)

    def on_render(self):
        frame = self.__create_frame()
        for b in self.bean_list:
            b.on_render(frame)
        self.player.on_render(frame)
        map.on_render(frame)
        return frame
        
    def __create_frame(self):
        frame = np.zeros((config.map_size[1] * config.tile_size, 
                          config.map_size[0] * config.tile_size, 3),
                             dtype=np.uint8)
        for i in range(config.map_size[0]):
            cv2.line(frame, 
                     (i * config.tile_size, 0),
                     (i * config.tile_size, config.map_size[1] * config.tile_size),
                     (120, 120, 120), 1)
        for i in range(config.map_size[1]):
            cv2.line(frame, 
                     (0, i * config.tile_size),
                     (config.map_size[0] * config.tile_size, i * config.tile_size),
                     (120, 120, 120), 1)
        return frame
    
    def show_win(self):
        frame = np.zeros((config.map_size[1] * config.tile_size, 
                          config.map_size[0] * config.tile_size, 3),
                             dtype=np.uint8)
        tex = "You Win!"
        cv2.putText(frame, tex, (40, 340), 
                    cv2.FONT_HERSHEY_DUPLEX,
                    4,
                    config.tex_color,
                    3, cv2.LINE_AA)
        return frame
    
gamemanager = GameManager()