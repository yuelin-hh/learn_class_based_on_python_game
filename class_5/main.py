from game_manager import gamemanager
from config import config

import cv2
import time

def main():
    cv2.namedWindow(config.window_name, cv2.WINDOW_AUTOSIZE)
    last = time.time()
    while(not config.is_end):
        key = cv2.waitKey(1) & 0xff
        if(cv2.getWindowProperty(config.window_name, cv2.WND_PROP_VISIBLE) < 1
           or key == 27):
            break

        gamemanager.on_input(key)
        now = time.time()
        delta = now - last
        if(delta <= 1 / config.fps):
            time.sleep(1 / config.fps - (delta))
            gamemanager.on_update(1 / config.fps)
        else:
            gamemanager.on_update(delta)
        last = time.time()

        frame = gamemanager.on_render()
        
        cv2.imshow(config.window_name, frame)

    frame = gamemanager.show_win()
    cv2.imshow(config.window_name, frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()