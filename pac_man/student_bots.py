"""学生策略模板：只修改两个 decide 方法中的寻路逻辑。

将本文件复制一份给每个小组，例如 team_a_bots.py，然后在 main.py 中传给
GameManager。不要修改 BattleState 或 GameManager，这样不同小组可以直接对战。
"""

try:
    from .interfaces import Direction
except ImportError:  # Running main.py directly from the pac_man directory.
    from interfaces import Direction


class StudentPacMan:
    def decide(self, state):
        # 示例：优先向最近的豆子移动。请替换成你们自己的算法。
        if not state.bean_positions:
            return None
        target = min(
            state.bean_positions,
            key=lambda bean: abs(bean[0] - state.pacman_position[0])
            + abs(bean[1] - state.pacman_position[1]),
        )
        for direction, position in state.neighbors(state.pacman_position):
            if position == target:
                return direction
        return next(iter(state.neighbors(state.pacman_position)), (None, None))[0]


class StudentGhost:
    def decide(self, state, ghost_index=0):
        # 示例：朝吃豆人距离变小的方向走。请替换成你们自己的算法。
        position = state.ghost_positions[ghost_index]
        choices = list(state.neighbors(position))
        if not choices:
            return None
        return min(
            choices,
            key=lambda item: abs(item[1][0] - state.pacman_position[0])
            + abs(item[1][1] - state.pacman_position[1]),
        )[0]

