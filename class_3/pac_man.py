from config import config
import cv2

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
        self.position = [320, 320]
        self.speed = 30
        self.direction = Direction.Right
        self.t = 0
        self.is_shut = False

    def on_input(self, key):
        if(key == ord('w')):
            self.direction = Direction.Up
        elif(key == ord('d')):
            self.direction = Direction.Right
        elif(key == ord('s')):
            self.direction = Direction.Down
        elif(key == ord('a')):
            self.direction = Direction.Left


    def on_update(self, delta):
        self.t += delta
        if (self.t >= self.frame_interval):
            self.t -= self.frame_interval
            self.is_shut = not self.is_shut
        self.__move(delta)

    def on_render(self, frame):
        center = (int(self.position[0]), int(self.position[1]))
        
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

    def __move(self, delta):
        if (self.direction == Direction.Up):
            self.position[1] -= self.speed * delta
        elif (self.direction == Direction.Down):
            self.position[1] += self.speed * delta
        elif (self.direction == Direction.Left):
            self.position[0] -= self.speed * delta
        elif (self.direction == Direction.Right):
            self.position[0] += self.speed * delta