from config import config
import pac_man

import cv2
import numpy as np

class GameManager:
    def __init__(self):
        self.player = pac_man.PacMan()

    def on_input(self, key):
        self.player.on_input(key)

    def on_update(self, delta):
        self.player.on_update(delta)

    def on_render(self):
        frame = self.__create_frame()
        self.player.on_render(frame)
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
    
gamemanager = GameManager()