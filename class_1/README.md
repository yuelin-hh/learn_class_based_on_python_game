# 第一节 创建你的游戏窗口

这一节是为了普及opencv常识，熟手可跳过

## part 1 创建一个入口

作为一个游戏，肯定需要一个运行入口，所以，我们先创建main.py

为了长远考虑，我们不可能将所有所有代码全部放在一个文件里，这样不利于阅读和管理

同时，为了保证入口的唯一性，我们不希望运行其他文件被导入时执行一些奇奇怪怪的脚本

所以我们先写下

```
def main():
    pass

if __name__ == "__main__":
    main()
```

这会保证只有直接运行main.py时才会执行main函数中的逻辑

## part 2 创建一个窗口

游戏肯定需要一个窗口，这部分我们交给opencv来负责(注：这只是为了简单，如果真的写游戏不会用python，更不会用opencv)

我们在加入

```
import cv2

def main():
    cv2.namedWindow("pac_man", cv2.WINDOW_AUTOSIZE)
```

一般情况下，你会看到一个窗口一闪而逝，这是因为创建完这个窗口后程序就立即结束了，如果你想看窗口的话，可以加个死循环卡住它

```
def main():
    cv2.namedWindow("pac_man", cv2.WINDOW_AUTOSIZE)
    while(True):
        pass
```

如果你运行了，你会发现你上当了，程序卡死了，窗口也关不掉，只能在命令行里用ctrl+C强制终止程序

注：如果你实在不会也可以打开任务管理器(ctrl+shift+esc)，前提是你在windows系统。然后搜一个叫Python的进程并杀死它

注注：如果这也不会可以双手离开键盘，并等待操作系统告诉你Python未响应然后再关掉它

这里坑你一下是希望你能了解程序卡死的解决方案，毕竟刚写完的代码能跑成什么样子只有上帝能知道

为了不会再出现窗口关不掉的情况，我们可以加上这段代码

```
def main():
    cv2.namedWindow("pac_man", cv2.WINDOW_AUTOSIZE)
    while(True):
        cv2.waitKey(1)
        if(cv2.getWindowProperty("pac_man", cv2.WND_PROP_VISIBLE) < 1):
            break
    cv2.destroyAllWindows()
```

现在你的窗口可以正常关闭了

cv2.getWindowProperty("pac_man", cv2.WND_PROP_VISIBLE) < 1 这一句会检查你的窗口是否关闭，如果是就跳出循环

cv2.waitKey(1)这一句是让窗口等待键盘输入1ms，防止全力循环燃尽你的CPU

cv2.destroyAllWindows()这一句是关闭所有窗口，及时释放资源是好习惯

## part 3 显示一帧图像

目前为止，你的窗口应该啥也没有，所以，我们给它加点东西

```
import numpy as np

def main():
    cv2.namedWindow("pac_man", cv2.WINDOW_AUTOSIZE)
    while(True):
        frame = np.zeros((640, 640, 3), dtype=np.uint8)
        cv2.imshow("pac_man", frame)
        cv2.waitKey(1)
        if(cv2.getWindowProperty("pac_man", cv2.WND_PROP_VISIBLE) < 1):
            break
    cv2.destroyAllWindows()

```

这下你的窗口应该会显示一个四四方方的黑色图片

import numpy as np 这句是导入numpy库并将其命名为np，numpy是opencv的底层支持，即opencv的图片全都是以numpy数组的形式进行存储的

但为什么要将它命名为np，作者也不知道(为了偷懒？)，只能说大家都这么写一定有他的道理

frame = np.zeros((640, 640, 3), dtype=np.uint8)这一句创建了一张尺寸为640 x 640的BGR三通道图像，储存格式是无符号八位整型

cv2.imshow("pac_man", frame)这一句是将frame图片渲染到窗口上

cv2.waitKey(1)此时，这一句不再是单纯的延时，而是担负起更重要的任务----强制刷新一帧画面，即如果单纯imshow没有waitkey画面是不会出现的，感兴趣的童鞋可以把这句注释掉看看

注意，opencv的图像是BGR而不是RGB这一点我们可以做一个尝试

```
while(True):
        frame = np.zeros((640, 640, 3), dtype=np.uint8)
        cv2.circle(frame, (320, 320), 200, (255, 0, 0), 5, cv2.LINE_AA)
        cv2.imshow("pac_man", frame)
        cv2.waitKey(1)
        if(cv2.getWindowProperty("pac_man", cv2.WND_PROP_VISIBLE) < 1):
            break
```

你会在窗口上看到一个蓝色的圆环

cv2.circle是opencv用于绘制圆的函数，还有其他很多绘制函数，我们不必全部详细了解，只要在有需要时去查找就可以了

（255， 0， 0）就是传入的绘制颜色，因为是BGR，所以第一个255指的是蓝色

至于为什么opencv用BGR而许多其他的库(如PIL，open_GL)用RGB，感兴趣的同学可以去自行研究