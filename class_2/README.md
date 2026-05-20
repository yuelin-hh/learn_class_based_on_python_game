# 第二节 创建游戏主循环

本节开始讲述游戏(程序)的设计架构

# part 1 游戏管理器

现在开始，我们要进行第一次抽象

我们创建game_manager.py并创建一个游戏管理器类

```
class GameManager:
    pass
```

为了保证每个模块功能尽量单一且独立，我们将游戏的主体内容都交给游戏管理器类来实现，主函数仅作为启动入口和处理主循环

正常的游戏主循环一般可以拆成三个板块：输入，更新，渲染

所以我们给GameManager类创建一个构造函数和三个类方法

```
class GameManager:
    def __init__(self):
        pass

    def on_input(self, key):
        pass

    def on_update(self, delta):
        pass

    def on_render(self):
        pass
```

我们希望整个程序中只存在一个GameManager类的实例(即单例类)，所以我们加上

```
gamemanager = GameManager()
```

然后修改一下主循环，使其更符合游戏的更新逻辑

```
def main():
    cv2.namedWindow("pac_man", cv2.WINDOW_AUTOSIZE)
    while(True):
        key = cv2.waitKey(1) & 0xff
        if(cv2.getWindowProperty("pac_man", cv2.WND_PROP_VISIBLE) < 1
           or key == 27):
            break

        # on_input

        # on_update

        # on_render
        frame = np.zeros((640, 640, 3), dtype=np.uint8)
        cv2.circle(frame, (320, 320), 200, (255, 0, 0), 5, cv2.LINE_AA)
        cv2.imshow("pac_man", frame)
    cv2.destroyAllWindows()
```

key == 27正好是esc的输入

但update更新还需要每一帧的间隔时间，所以我们加上

```
def main():
    cv2.namedWindow("pac_man", cv2.WINDOW_AUTOSIZE)
    last = time.time()
    while(True):
        key = cv2.waitKey(1) & 0xff
        if(cv2.getWindowProperty("pac_man", cv2.WND_PROP_VISIBLE) < 1
           or key == 27):
            break

        # on_input
        now = time.time()
        delta = now - last
        last = now
        # on_update

        # on_render
        frame = np.zeros((640, 640, 3), dtype=np.uint8)
        cv2.circle(frame, (320, 320), 200, (255, 0, 0), 5, cv2.LINE_AA)
        cv2.imshow("pac_man", frame)
    cv2.destroyAllWindows()
```

求得帧间隔

然后把主循环里的渲染逻辑移动到GameManager的on_render方法里

```
    def on_render(self):
        frame = np.zeros((640, 640, 3), dtype=np.uint8)
        cv2.circle(frame, (320, 320), 200, (255, 0, 0), 5, cv2.LINE_AA)
        return frame
```

然后在主循环调用GameManager的类方法

```
while(True):
    key = cv2.waitKey(1) & 0xff
    if(cv2.getWindowProperty("pac_man", cv2.WND_PROP_VISIBLE) < 1
       or key == 27):
        break
    gamemanager.on_input(key)
    now = time.time()
    delta = now - last
    last = now
    gamemanager.on_update(delta)
    frame = gamemanager.on_render()
    
    cv2.imshow("pac_man", frame)
```

注意要先在开头引入gamemanager单例

```
from game_manager import gamemanager
```

运行程序，发现和之前别无二致

# part 2 帧率控制

现在的程序还是在拼了命地跑，但实际上我们并不需要这么高的帧率

为了CPU着想，我们限制一下它的帧率

```
def main():
    cv2.namedWindow("pac_man", cv2.WINDOW_AUTOSIZE)
    last = time.time()
    fps = 60
    while(True):
        key = cv2.waitKey(1) & 0xff
        if(cv2.getWindowProperty("pac_man", cv2.WND_PROP_VISIBLE) < 1
           or key == 27):
            break

        gamemanager.on_input(key)
        now = time.time()
        delta = now - last
        if(delta <= 1 / fps):
            time.sleep(1 / fps - (delta))
            gamemanager.on_update(1 / fps)
        else:
            gamemanager.on_update(delta)
        last = time.time()

        frame = gamemanager.on_render()
        
        cv2.imshow("pac_man", frame)
    cv2.destroyAllWindows()
```

在一帧时间低于平均时间时通过睡觉把这个时间补上，可以打开任务管理器看看cpu占用率是不是有所下降(理论上不会降多少，因为waitkey存在，最高也就1000帧)

# part 3 配置文件

将项目的各个参数散落在文件各处是很不好的习惯，比如你想修改什么参数的时候可能会出现漏改的情况

别人在读你的代码时也会对着一堆数字感到不知所云

在写c++程序时更是这样，硬编码的参数每次修改都要重新编译一大串文件，非常浪费时间

所以，要有一个东西专门来管理配置信息

创建config.py，并创建Config类

```
class Config:
    pass
```

我们希望配置信息在全局是唯一的

所以照例将其单例化

```
config = Config()
```

我们可以把目前用到的配置参数都存入config中

```
class Config:
    window_name = "pac_man"
    fps = 60
    window_width = 640
    window_height = 640
```

然后调用它们

```
from config import config

def main():
    cv2.namedWindow(config.window_name, cv2.WINDOW_AUTOSIZE)
    last = time.time()
    while(True):
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
    cv2.destroyAllWindows()
```

```
from config import config

class GameManager:
    def __init__(self):
        pass

    def on_input(self, key):
        pass

    def on_update(self, delta):
        pass

    def on_render(self):
        frame = np.zeros((config.window_height, config.window_width, 3), dtype=np.uint8)
        cv2.circle(frame, (320, 320), 200, (255, 0, 0), 5, cv2.LINE_AA)
        return frame
```

这样一来代码的可读性和可修改性就提高了