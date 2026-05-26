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
        frame = np.zeros((config.window_height, config.window_width, 3), dtype=np.uint8)
        self.player.on_render(frame)
        return frame
        
gamemanager = GameManager()