# 第三节 创建角色

本节教你怎么让你的吃豆人动起来

## part 1 pac_man类

创建pac_man.py并创建我们的角色类

```
class PacMan:
    pass
```

按照输入、更新、渲染的流程为其填入函数

```
class PacMan:
    def __init__(self):
        pass

    def on_input(self, key):
        pass

    def on_update(self, delta):
        pass

    def on_render(self, frame):
        pass
```

## part 2 画一个吃豆人

咱们现在来尝试实现一个嘴巴一张一闭的吃豆人

最简单的实现方式就是计时切换嘴巴开与闭的状态

在config.py中加入吃豆人相关的配置

```
class PacManConfig:
    radious = 16
    frame_interval = 0.2
    color = (0, 240, 255)

class Config:
    pacman_config = PacManConfig()
    window_name = "pac_man"
    fps = 60
    window_width = 640
    window_height = 640
```

然后在吃豆人类里加载

```
from config import config

class PacMan:
    def __init__(self):
        self.radious = config.pacman_config.radious
        self.frame_interval = config.pacman_config.frame_interval
        self.color = config.pacman_config.color
```

定时切换嘴巴开闭的逻辑很好实现，我们只需要一个变量记录时间，一个变量记录状态

```
def __init__(self):
    self.radious = config.pacman_config.radious
    self.frame_interval = config.pacman_config.frame_interval
    self.color = config.pacman_config.color
    self.angle = config.pacman_config.angle
    self.t = 0
    self.is_shut = False
```

然后在on_update方法里更新这两个变量

```
def on_update(self, delta):
        self.t += delta
        if (self.t >= self.frame_interval):
            self.t -= self.frame_interval
            self.is_shut = not self.is_shut
```

最后在on_render方法里用opencv的绘制函数渲染

```
def on_render(self, frame):
    center = (320, 320)
    
    if(self.is_shut):
        cv2.ellipse(
            frame,
            center,
            axes=(self.radious, self.radious),
            angle=0,
            startAngle=0,
            endAngle=360,
            color=self.color,
            thickness=-1,
            lineType=cv2.LINE_AA
        )
    else:
        cv2.ellipse(
            frame,
            center,
            axes=(self.radious, self.radious),
            angle=0,
            startAngle=self.angle/2,
            endAngle=360 - self.angle/2,
            color=self.color,
            thickness=-1,
            lineType=cv2.LINE_AA
        )
```

因为没有移动逻辑，我们暂时把吃豆人的位置定在(320, 320)

于是，我们就可以在game_manager里加上pac_man的实例了

```
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
```

运行main.py就可以看到一个黄色的吃豆人了

## part 3 让吃豆人动起来

让吃豆人动起来很简单，只需要在on_input方法中加入逻辑就可以了

为了让画面更加好看，我们给吃豆人加上四个方向

```
from enum import Enum

class Direction(Enum):
    Right = 0
    Down = 1
    Left = 2
    Up = 3

class PacMan:
    def __init__(self):
        self.radious = config.pacman_config.radious
        self.frame_interval = config.pacman_config.frame_interval
        self.color = config.pacman_config.color
        self.angle = config.pacman_config.angle
        self.direction = Direction.Right
        self.t = 0
        self.is_shut = False
```

加上输入逻辑，使其根据WASD改变方向

```
def on_input(self, key):
    if(key == ord('w')):
        self.direction = Direction.Up
    elif(key == ord('d')):
        self.direction = Direction.Right
    elif(key == ord('s')):
        self.direction = Direction.Down
    elif(key == ord('a')):
        self.direction = Direction.Left
```

更改渲染逻辑，让其开口朝向direction

```
def on_render(self, frame):
    center = (320, 320)
    
    if(self.is_shut):
        cv2.ellipse(
            frame,
            center,
            axes=(self.radious, self.radious),
            angle=0,
            startAngle=0,
            endAngle=360,
            color=self.color,
            thickness=-1,
            lineType=cv2.LINE_AA
        )
    else:
        cv2.ellipse(
            frame,
            center,
            axes=(self.radious, self.radious),
            angle=90 * self.direction.value,
            startAngle=self.angle/2,
            endAngle=360 - self.angle/2,
            color=self.color,
            thickness=-1,
            lineType=cv2.LINE_AA
        )
```

运行main.py吃豆人就会改变方向了

我们希望吃豆人在一个网格状的地图中移动，但这就不得不依赖map类，本节暂不涉及

简单起见，我们让吃豆人一直向面朝的方向移动

首先保存position和speed变量

```
self.position = [320, 320]
self.speed = 30
```

然后在on_update方法里更新它，简单起见，我们单开一个__move函数

```
def __move(self, delta):
    if (self.direction == Direction.Up):
        self.position[1] -= self.speed * delta
    elif (self.direction == Direction.Down):
        self.position[1] += self.speed * delta
    elif (self.direction == Direction.Left):
        self.position[0] -= self.speed * delta
    elif (self.direction == Direction.Right):
        self.position[0] += self.speed * delta
```

并在on_update里调用它

```
def on_update(self, delta):
    self.t += delta
    if (self.t >= self.frame_interval):
        self.t -= self.frame_interval
        self.is_shut = not self.is_shut
    self.__move(delta)
```

最后在on_render里让中心变为opsition

```
def on_render(self, frame):
    center = (int(self.position[0]), int(self.position[1]))
```

记得要把中心坐标从float转成int

运行就会发现吃豆人会朝前方移动了