# 第四节 在地图中移动

本节教你如何创建一个瓦片地图

# part 1 绘制地图网格

我们先在config中加入地图的配置

```
class Config:
    pacman_config = PacManConfig()
    window_name = "pac_man"
    fps = 60
    map_size = (16, 16)
    tile_size = 40
```

map_size即为地图横向与纵向的瓦片数量

tile_size即为瓦片的尺寸（像素）

有了它们我们便不再需要窗口的尺寸了

为game_manager创建一个__create_frame方法，并在on_render方法中调用它

```
def on_render(self):
    frame = self.__create_frame()
    self.player.on_render(frame)
    return frame
    
def __create_frame(self):
    frame = np.zeros((config.map_size[1] * config.tile_size, 
                      config.map_size[0] * config.tile_size, 3),
                         dtype=np.uint8)
    for i in range(config.map_size[0]):
        cv2.line(frame, 
                 (i * config.tile_size, 0),
                 (i * config.tile_size, config.map_size[1] * config.tile_size),
                 (120, 120, 120), 1)
    for i in range(config.map_size[1]):
        cv2.line(frame, 
                 (0, i * config.tile_size),
                 (config.map_size[0] * config.tile_size, i * config.tile_size),
                 (120, 120, 120), 1)
    return frame
```

运行main.py我们就可以看到灰色的线条将地图分割成了一个个网格

# part 2 让吃豆人在网格中移动

为了能让角色在网格中移动，必须把角色位置从像素坐标更改为网格坐标

在配置文件中加入

```
class PacManConfig:
    radious = 16
    frame_interval = 0.2
    color = (0, 240, 255)
    angle = 50
    speed = 3
    position = [8, 8]
```

并让pac_man类读取

```
def __init__(self):
    self.radious = config.pacman_config.radious
    self.frame_interval = config.pacman_config.frame_interval
    self.color = config.pacman_config.color
    self.angle = config.pacman_config.angle
    self.position = config.pacman_config.position
    self.speed = config.pacman_config.speed
    self.direction = Direction.Right
    self.t = 0
    self.is_shut = False
```

同时调整渲染逻辑，让其能正确地从地图坐标系映射到像素坐标系

```
def on_render(self, frame):
    center = (int((self.position[0] + 0.5) * config.tile_size),
               int((self.position[1] + 0.5) * config.tile_size))
    ...
```

现在它不再局限在一个角落里了，但依然不能按网格移动

此处我给出的解法是输入时储存目标网格的坐标，然后移动到该网格

我们在pac_man中加上

```
def __init__(self):
    ...
    self.is_moving = False
    self.target = self.position
```

target储存下一个要到达的网格

is_moving判断是否在这个网格到目标网格的移动过程中

然后由on_input方法根据输入判断目标位置

```
def on_input(self, key):
    if(self.is_moving):
        return
    
    if(key == ord('w')):
        self.direction = Direction.Up
        self.target = [self.position[0], self.position[1] - 1]
        self.is_moving = True
    elif(key == ord('d')):
        self.direction = Direction.Right
        self.target = [self.position[0] + 1, self.position[1]]
        self.is_moving = True
    elif(key == ord('s')):
        self.direction = Direction.Down
        self.target = [self.position[0], self.position[1] + 1]
        self.is_moving = True
    elif(key == ord('a')):
        self.direction = Direction.Left
        self.target = [self.position[0] - 1, self.position[1]]
        self.is_moving = True
```

我们希望在移动过程中不更新下一个网格，也不更新方向

接着，要在__move方法中修改移动逻辑

```
def __move(self, delta):
    if(not self.is_moving):
        return
    
    if (self.direction == Direction.Right):
        self.position[0] += self.speed * delta
        if(self.position[0] >= self.target[0]):
            self.position[0] = self.target[0]
            self.is_moving = False
    elif (self.direction == Direction.Up):
        self.position[1] -= self.speed * delta
        if(self.position[1] <= self.target[1]):
            self.position[1] = self.target[1]
            self.is_moving = False
    elif (self.direction == Direction.Down):
        self.position[1] += self.speed * delta
        if(self.position[1] >= self.target[1]):
            self.position[1] = self.target[1]
            self.is_moving = False
    elif (self.direction == Direction.Left):
        self.position[0] -= self.speed * delta
        if(self.position[0] <= self.target[0]):
            self.position[0] = self.target[0]
            self.is_moving = False
```

这样我们的吃豆人就可以正确在网格中移动了

# part 3 让吃豆人正确地移动

如果多试一试就会发现，我们的地图没有边界检查，即吃豆人可以跑出地图

所以我们必须要在输入阶段检查目标网格是否合法

在pac_man类里加入__check_can_move方法

```
def __check_can_move(self):
    if (self.target[0] < 0 or 
        self.target[0] > config.map_size[0] - 1 or
        self.target[1] < 0 or 
        self.target[1] > config.map_size[1] - 1):
        self.target = self.position
    else:
        self.is_moving = True
```

并在on_input方法中调用

```
def on_input(self, key):
    if(self.is_moving):
        return
    
    if(key == ord('w')):
        self.direction = Direction.Up
        self.target = [self.position[0], self.position[1] - 1]
        self.__check_can_move()
    elif(key == ord('d')):
        self.direction = Direction.Right
        self.target = [self.position[0] + 1, self.position[1]]
        self.__check_can_move()
    elif(key == ord('s')):
        self.direction = Direction.Down
        self.target = [self.position[0], self.position[1] + 1]
        self.__check_can_move()
    elif(key == ord('a')):
        self.direction = Direction.Left
        self.target = [self.position[0] - 1, self.position[1]]
        self.__check_can_move()
```

这样我们的吃豆人就不会逃出地图了