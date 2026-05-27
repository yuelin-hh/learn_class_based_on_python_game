# 第五节 墙体和豆子

本节进行最后首尾，实现豆子和墙体的功能

## part 1 墙体

创建map.py在其中创建Map类，并让其单例

```
class Map:
    pass

map = Map()
```

我们希望墙体在格子与格子的交界处，于是我们想到用两个二维列表分别存储横向与纵向的墙体

```
class Map:
    def __init__(self):
        self.wall_h = [[False for j in range(config.map_size[1] + 1)]
                        for i in range(config.map_size[0])]
        self.wall_v = [[False for j in range(config.map_size[1])]
                        for i in range(config.map_size[0] + 1)]
```

这两个列表囊括了所有网格的边，用True和False来表示是否有墙体

然后我们创建MapConfig来储存墙体的配置文件

```
class MapConfig:
    wall_color = (240, 240, 40)
    wall_h_list = [
        (1, 4, 1), (12, 15, 1),
        (2, 14, 2),
        (3, 6, 3), (10, 13, 3),
        (1, 3, 4), (13, 15, 4),
        (4, 6, 4), (10, 12, 4),
        (5, 11, 5),
        (4, 6, 9), (7, 9, 9), (10, 12, 9),
        (0, 3, 11), (13, 16, 11),
        (1, 2, 12), (4, 6, 12), (10, 12, 12), (14, 15, 12),
        (6, 10, 14),
        (5, 7, 15), (9, 11, 15),

    ]
    wall_v_list = [
        (8, 0, 1),
        (1, 1, 3), (15, 1, 3),
        (6, 3, 4), (10, 3, 4),
        (8, 3, 5),
        (4, 4, 8), (12, 4, 8),
        (2, 4, 10), (14, 4, 10),
        (7, 7, 9), (9, 7, 9),
        (3, 7, 11), (13, 7, 11),
        (6, 9, 12), (10, 9, 12),
        (1, 12, 15), (15, 12, 15),
        (8, 11, 14),
        (3, 14, 16), (13, 14, 16),
        (5, 13, 15), (11, 13, 15),
    ]

class Config:
    pacman_config = PacManConfig()
    map_config = MapConfig()
    window_name = "pac_man"
    fps = 60
    map_size = (16, 16)
    tile_size = 40
```

此处我就直接使用已经写好的墙体配置

wall_h_list存储水平的墙体，结构为(左端点，右端点，纵坐标)

wall_v_list存储垂直的墙体，结构为(横坐标，上端点，下端点)

我们在map类的构造函数中读取这些配置，同时为地图边缘生成一圈墙体

```
def __init__(self):
        self.wall_h = [[False for j in range(config.map_size[1] + 1)]
                        for i in range(config.map_size[0])]
        self.wall_v = [[False for j in range(config.map_size[1])]
                        for i in range(config.map_size[0] + 1)]
        for i in range(config.map_size[0]):
            self.wall_h[i][0] = True
            self.wall_h[i][config.map_size[1]] = True
        for j in range(config.map_size[1]):
            self.wall_v[0][j] = True
            self.wall_v[config.map_size[0]][j] = True
        
        for w in config.map_config.wall_h_list:
            for i in range(w[0], w[1]):
                try:
                    self.wall_h[i][w[2]] = True
                except:
                    pass
        for w in config.map_config.wall_v_list:
            for i in range(w[1], w[2]):
                try:
                    self.wall_v[w[0]][i] = True
                except:
                    pass
```

我们试着将它们绘制出来

```
def on_render(self, frame):
    for i in range(config.map_size[0]):
        for j in range(config.map_size[1] + 1):
            if(self.wall_h[i][j]):
                cv2.line(frame, 
                         (i * config.tile_size, j * config.tile_size - 1),
                         ((i+ 1) * config.tile_size, j * config.tile_size - 1),
                         config.map_config.wall_color, 3)
    for i in range(config.map_size[0] + 1):
        for j in range(config.map_size[1]):
            if(self.wall_v[i][j]):
                cv2.line(frame, 
                         (i * config.tile_size - 1, j * config.tile_size),
                         (i * config.tile_size - 1, (j + 1) * config.tile_size),
                         config.map_config.wall_color, 3)
```

可以看到我们已经能够正确创建墙体了，接下来只要为墙体填充功能就行

我的方案是通过一个check_wall方法来检查position和target之间是否有墙体

```
def check_wall(self, position, target):
    if(position[0] == target[0] and position[1] == target[1]):
        return True
    elif(position[0] == target[0] and position[1] != target[1]):
        if(position[1] < target[1]):
            return self.wall_h[position[0]][target[1]]
        else:
            return self.wall_h[position[0]][position[1]]
    elif(position[0] != target[0] and position[1] == target[1]):
        if(position[0] < target[0]):
            return self.wall_v[target[0]][position[1]]
        else:
            return self.wall_v[position[0]][position[1]]
```

于是只要修改pac_man的__check_can_move方法就行

```
def __check_can_move(self):
    if(map.check_wall(self.position, self.target)):
        self.target = self.position
    else:
        self.is_moving = True
```

此时墙体便有了作用

## part 2 豆子

豆子的逻辑非常简单，只有一个闪烁和被吃检测

依旧先创建配置文件

```
class BeanConfig:
    color = (0, 160, 160)
    color_shining = (0, 240, 255)
    frame_interval = 0.5
    radious = 2
    positions = [ 
        (3, 3)
    ]

class Config:
    bean_config = BeanConfig()
    pacman_config = PacManConfig()
    map_config = MapConfig()
    window_name = "pac_man"
    fps = 60
    map_size = (16, 16)
    tile_size = 40
    eat_range = 0.2
    is_end = False
```

is_end用来判断豆子是否吃完，要不要退出主循环

然后创建bean.py文件，填入内容

因为内容相当重复，所以直接附上源码

```
from config import config

import numpy as np
import cv2

class Bean:
    def __init__(self, position = (8, 8)):
        self.position = position
        self.color = config.bean_config.color
        self.color_shining = config.bean_config.color_shining
        self.radious = config.bean_config.radious
        self.frame_interval = config.bean_config.frame_interval
        r = np.random.normal(0, 0.01)
        if (r + self.frame_interval > 0):
            self.frame_interval += r

        self.t = np.random.normal(0, self.frame_interval)
        self.is_shing = False

    def on_update(self, delta):
        self.t += delta
        if (self.t >= self.frame_interval):
            self.t -= self.frame_interval
            self.is_shing = not self.is_shing
    
    def on_render(self, frame):
        center = (int((self.position[0] + 0.5) * config.tile_size),
                   int((self.position[1] + 0.5) * config.tile_size))
        if(self.is_shing):
            cv2.circle(frame, center, self.radious,
                       self.color_shining, -1, cv2.LINE_AA)
        else:
            cv2.circle(frame, center, self.radious,
                       self.color, -1, cv2.LINE_AA)
            
def check_eat(man_position, bean_position):
    distace = ((man_position[0] - bean_position[0]) ** 2 + 
               (man_position[1] - bean_position[1]) ** 2)
    if distace <= config.eat_range ** 2:
        return True
    else:
        return False
```

然后在game_manager类里用一个列表来存储所有豆子

```
class GameManager:
    def __init__(self):
        self.player = pac_man.PacMan()
        self.bean_list = []
        for p in config.bean_config.positions:
            self.bean_list.append(bean.Bean(p))
```

然后添加更新和渲染逻辑

```
def on_update(self, delta):
    self.player.on_update(delta)
    to_remove = [b for b in self.bean_list if bean.check_eat(self.player.position, b.position)]
    for b in to_remove:
        self.bean_list.remove(b)
    for b in self.bean_list:
        b.on_update(delta)
def on_render(self):
    frame = self.__create_frame()
    for b in self.bean_list:
        b.on_render(frame)
    self.player.on_render(frame)
    map.on_render(frame)
    return frame
```

然后就会出现一个闪烁的黄色豆子

但现在吃掉这个豆子并不会退出循环

我们在game_manager中加上豆子是否吃完的逻辑

```
def on_update(self, delta):
    self.player.on_update(delta)
    to_remove = [b for b in self.bean_list if bean.check_eat(self.player.position, b.position)]
    for b in to_remove:
        self.bean_list.remove(b)
    if (len(self.bean_list) == 0):
        config.is_end = True
        return
    for b in self.bean_list:
        b.on_update(delta)
```

同时改变主循环的判断

```
def main():
    cv2.namedWindow(config.window_name, cv2.WINDOW_AUTOSIZE)
    last = time.time()
    while(not config.is_end):
    ...
```
这样就会正常结束了

我们希望每个格子都有一个豆子，但是一个一个写进配置文件太麻烦了，我们可以偷点懒

```
class Config:
    def __init__(self):
        self.__init_bean_position()

    def __init_bean_position(self):
        self.bean_config.positions.clear()
        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                self.bean_config.positions.append((i, j))
```

如此，直接在config文件里加一个初始化逻辑，就能看到满屏的豆子了

## part 3 最后的优化

现在我们程序的功能已经基本实现了，但游玩时我们会发现吃豆人的操作会有点卡手

所以，我们考虑加一个预输入的功能

先为吃豆人加一个last_key属性记录在移动中的最后一次输入

```
class PacMan:
    def __init__(self):
        ...
        self.last_key = 255
```

然后在on_input方法中更新last_key，并在后续输入中调用

```
def on_input(self, key):
    if(self.is_moving):
        if (key != 255):
            self.last_key = key
        return
    
    if (self.last_key != 255 and key == 255):
        key = self.last_key
        self.last_key = 255

    ...
```

同时记得在__check_can_move中加一句

```
def __check_can_move(self):
        if(map.check_wall(self.position, self.target)):
            self.target = self.position
        else:
            self.is_moving = True
        self.last_key = 255
```

然后操作起来就比较流畅了

最后再加一个结算动画

在game_manager中加入show_win方法

```
def show_win(self):
    frame = np.zeros((config.map_size[1] * config.tile_size, 
                      config.map_size[0] * config.tile_size, 3),
                         dtype=np.uint8)
    tex = "You Win!"
    cv2.putText(frame, tex, (40, 340), 
                cv2.FONT_HERSHEY_DUPLEX,
                4,
                config.tex_color,
                3, cv2.LINE_AA)
    return frame
```

别忘了config里也加上

```
class Config:
    ...
    tex_color = (0, 240, 255)
```

在main函数主循环外加上

```
def main():
    cv2.namedWindow(config.window_name, cv2.WINDOW_AUTOSIZE)
    last = time.time()
    while(not config.is_end):
        ...

    frame = gamemanager.show_win()
    cv2.imshow(config.window_name, frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

这样吃完豆子就会弹出结算动画了