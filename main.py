from math import *
import random

landmarks = [[20.0, 20.0],
             [80.0, 80.0],
             [20.0, 80.0],
             [80.0, 20.0]]

world_size = 100.0


class robot:
    def __init__(self):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2 * pi
        self.forward_noise = 0.0
        self.turn_noise = 0.0
        self.sense_noise = 0.0

    def set(self, x, y, orient):
        if x < 0 or x >= world_size:
            raise ValueError('X out of coordinates')
        if y < 0 or y >= world_size:
            raise ValueError('Y out of coordinates')
        if orient < 0 or orient >= 2 * pi:
            raise ValueError('Orientation must be [0...2pi]')
        self.x = float(x)
        self.y = float(y)
        self.orientation = float(orient)

    def set_noise(self, f_noise, t_noise, s_noise):
        # SET NOISE DATA FOR PARTICLE FILTER
        self.forward_noise = f_noise
        self.turn_noise = t_noise
        self.sense_noise = s_noise

    def __str__(self):
        return "[x={0} y={1} heading={2}]".format(self.x, self.y, self.orientation)


def main():
    myrobot = robot()
    myrobot.set(10.0, 10.0, 0.0)
    print(myrobot)


if __name__ == '__main__':
    main()
