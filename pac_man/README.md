### 运行

```
# 先cd进入learn_class_based_on_python_game目录
python3 ./pac_man/main.py
```

### 操作

默认由 A* 自动鬼和自动吃豆人进行对战，窗口会实时显示剩余豆子和比赛用时。
鬼每两回合移动一格，每次移动都会重新用 A* 计算通往吃豆人的最短路径；
这样它仍然具有追击能力，也给吃豆人留下观察和躲避的机会。

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
逻辑。参考实现位于 `strategies.py`，寻路器位于 `pathfinding.py`。然后在
`main.py` 的策略组装位置替换两个对象：

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

#### 两个核心类

`AStarPathfinder` 只负责图搜索：它从 `BattleState` 读取可行方向，用
`f(n) = g(n) + h(n)` 选择下一个格子，其中 `g(n)` 是已经走过的步数，
`h(n)` 是到目标格子的曼哈顿距离。

`AStarGhostBrain` 在每次移动时以鬼的位置为起点、吃豆人的位置为目标调用
A*。`AutoPacManBrain` 使用相同的移动节奏预测鬼的下一步，排除会碰撞或
交换位置的动作，再做多步逃生判断，最后从安全动作中选择“豆子更近、
离鬼更远、出口更多”的一步。

关于类之间的职责、A* 公式和自动吃豆人的决策过程，可以继续阅读
[`OOP_WALKTHROUGH.md`](./OOP_WALKTHROUGH.md)。

#### 自动测试

```bash
cd pac_man
python3 -m unittest -v test_strategies.py
```

测试会检查 A* 路径的每一步都合法，并模拟一整局，确认自动吃豆人能吃完
256 个豆子且不被鬼抓到。
