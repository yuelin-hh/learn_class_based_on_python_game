import os
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

try:
    from .game_manager import GameManager
    from .strategies import AStarGhostBrain, AutoPacManBrain
    from .config import config
except ImportError:  # Running main.py directly from the pac_man directory.
    from game_manager import GameManager
    from strategies import AStarGhostBrain, AutoPacManBrain
    from config import config

import cv2
import time

# 课堂上只需要替换这两个对象，不要修改游戏循环。
# from team_a_bots import StudentPacMan
# from team_b_bots import StudentGhost
gamemanager = GameManager(
    pacman_brain=AutoPacManBrain(),
    ghost_brains=[AStarGhostBrain()],
)

def main():
    cv2.namedWindow(config.window_name, cv2.WINDOW_AUTOSIZE)
    last = time.time()
    while (not config.is_end):
        key = cv2.waitKey(1)  & 0xFF
        if(key == 27 or 
           cv2.getWindowProperty(config.window_name, cv2.WND_PROP_VISIBLE) < 1):
            cv2.destroyAllWindows()
            return
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
