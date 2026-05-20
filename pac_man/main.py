import os
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

from game_manager import gamemanager
from config import config

import cv2
import time

def main():
    cv2.namedWindow("pac_man", cv2.WINDOW_AUTOSIZE)
    last = time.time()
    while (not config.is_end):
        key = cv2.waitKey(10)  & 0xFF
        if(key == 27 or 
           cv2.getWindowProperty("pac_man", cv2.WND_PROP_VISIBLE) < 1):
            cv2.destroyAllWindows()
            return
        gamemanager.on_input(key)
        now = time.time()
        if(now - last <= 0.01):
            time.sleep(0.01 - (now - last))
            gamemanager.on_update(0.01)
        else:
            gamemanager.on_update(now - last)

        frame = gamemanager.on_render()
        cv2.imshow("pac_man", frame)
        last = time.time()

    frame = gamemanager.show_win()
    cv2.imshow("pac_man", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()