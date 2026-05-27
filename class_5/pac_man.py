from config import config
from map import map
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
        self.position = config.pacman_config.position
        self.speed = config.pacman_config.speed
        self.direction = Direction.Right
        self.t = 0
        self.is_shut = False
        self.is_moving = False
        self.target = self.position
        self.last_key = 255

    def on_input(self, key):
        if(self.is_moving):
            if (key != 255):
                self.last_key = key
            return
        
        if (self.last_key != 255 and key == 255):
            key = self.last_key
            self.last_key = 255
        
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


    def on_update(self, delta):
        self.t += delta
        if (self.t >= self.frame_interval):
            self.t -= self.frame_interval
            self.is_shut = not self.is_shut
        self.__move(delta)

    def on_render(self, frame):
        center = (int((self.position[0] + 0.5) * config.tile_size),
                   int((self.position[1] + 0.5) * config.tile_size))
        
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

    def __check_can_move(self):
        if(map.check_wall(self.position, self.target)):
            self.target = self.position
        else:
            self.is_moving = True
        self.last_key = 255