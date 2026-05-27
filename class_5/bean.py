from config import config

import numpy as np
import cv2

class Bean:
    def __init__(self, position = (8, 8)):
        self.position = position
        self.color = config.bean_config.color
        self.color_shining = config.bean_config.color_shining
        self.radious = config.bean_config.radious
        self.frame_interval = config.bean_config.frame_interval
        r = np.random.normal(0, 0.01)
        if (r + self.frame_interval > 0):
            self.frame_interval += r

        self.t = np.random.normal(0, self.frame_interval)
        self.is_shing = False

    def on_update(self, delta):
        self.t += delta
        if (self.t >= self.frame_interval):
            self.t -= self.frame_interval
            self.is_shing = not self.is_shing
    
    def on_render(self, frame):
        center = (int((self.position[0] + 0.5) * config.tile_size),
                   int((self.position[1] + 0.5) * config.tile_size))
        if(self.is_shing):
            cv2.circle(frame, center, self.radious,
                       self.color_shining, -1, cv2.LINE_AA)
        else:
            cv2.circle(frame, center, self.radious,
                       self.color, -1, cv2.LINE_AA)
            
def check_eat(man_position, bean_position):
    distace = ((man_position[0] - bean_position[0]) ** 2 + 
               (man_position[1] - bean_position[1]) ** 2)
    if distace <= config.eat_range ** 2:
        return True
    else:
        return False