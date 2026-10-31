### 运行

```
# 先cd进入learn_class_based_on_python_game目录
python3 ./pac_man/main.py
```

### 操作

默认由两个自动策略进行对战，窗口会实时显示剩余豆子和比赛用时。

吃完所有豆子后，结算画面会显示最终用时；如果被鬼抓到，则显示失败时的用时。

按下esc或关闭窗口退出

### 对战教学模式

`pac_man` 支持“自动吃豆人 vs 自动鬼”的对战。地图、碰撞、吃豆和结算由
`GameManager` 负责，每个学生只需要实现一个 `decide` 方法。

#### 调用接口

```python
from interfaces import Direction

class MyPacMan:
    def decide(self, state):
        # 返回 Direction，或者返回 None 表示原地等待
        for direction, target in state.neighbors(state.pacman_position):
            if target in state.bean_positions:
                return direction
        return None

class MyGhost:
    def decide(self, state, ghost_index=0):
        position = state.ghost_positions[ghost_index]
        return state.neighbors(position)[0][0]
```

`state` 提供 `turn`、`map_size`、`pacman_position`、`ghost_positions`、
`bean_positions`，以及 `neighbors(position)` 和 `can_move(position, direction)`。
坐标都是 `(x, y)` 格子坐标；方向只能从 `Direction.RIGHT`、`DOWN`、`LEFT`、
`UP` 中选择。`state` 是只读快照，策略不应直接修改它或访问 `GameManager`。

#### 运行不同小组的代码

把 `student_bots.py` 复制成每个小组自己的文件，只修改 `decide` 中的寻路
逻辑。然后在 `main.py` 的策略组装位置替换两个对象：

```python
from team_a_bots import StudentPacMan
from team_b_bots import StudentGhost
from game_manager import GameManager

gamemanager = GameManager(
    pacman_brain=StudentPacMan(),
    ghost_brains=[StudentGhost()],
)
```

窗口演示直接运行 `python main.py`。默认使用 `strategies.py` 中的参考策略；
比赛过程和计时都会在窗口中展示。
