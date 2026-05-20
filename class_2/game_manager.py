from config import config

import cv2
import numpy as np

class GameManager:
    def __init__(self):
        pass

    def on_input(self, key):
        pass

    def on_update(self, delta):
        pass

    def on_render(self):
        frame = np.zeros((config.window_height, config.window_width, 3), dtype=np.uint8)
        cv2.circle(frame, (320, 320), 200, (255, 0, 0), 5, cv2.LINE_AA)
        return frame
        
gamemanager = GameManager()