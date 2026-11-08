"""学生策略模板：A* 鬼 + 自动吃豆并躲避的吃豆人。

将本文件复制一份给每个小组，例如 team_a_bots.py，然后在 main.py 中传给
GameManager。不要修改 BattleState 或 GameManager，这样不同小组可以直接对战。
"""

try:
    from .strategies import AStarGhostBrain, AutoPacManBrain
except ImportError:  # Running main.py directly from the pac_man directory.
    from strategies import AStarGhostBrain, AutoPacManBrain


class StudentPacMan(AutoPacManBrain):
    """自动吃豆人：评价每个安全动作，兼顾吃豆进度和逃生空间。"""


class StudentGhost(AStarGhostBrain):
    """追击鬼：使用 A* 找到通往吃豆人的最短路径。"""

