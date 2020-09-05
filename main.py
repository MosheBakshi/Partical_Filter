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
        self.forward_noise = float(f_noise)
        self.turn_noise = float(t_noise)
        self.sense_noise = float(s_noise)

    def sense(self):
        Z = []
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z

    def move(self, turn, forward):
        if forward < 0:
            raise ValueError("Robot can't move backwards")
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi

        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= world_size
        y %= world_size

        # create particle
        res = robot()
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res

    def Gaussian(self, mu, sigma, x):
        return (1.0 / sqrt(2.0 * pi * (sigma ** 2))) * exp(- ((mu - x) ** 2) / sigma)

    def measurement_prob(self, measurement):
        prob = 1.0
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob

    def __str__(self):
        return "[x=%.6s y=%.6s heading=%.6s]" % (self.x, self.y, self.orientation)

def eval(r, p):
    sum = 0.0;
    for i in range(len(p)):    # calculate mean error
        dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
        dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))


def main():
    myrobot = robot()
    myrobot = myrobot.move(0.1, 5)
    Z = myrobot.sense()
    # print(Z)
    # print(myrobot)
    N = 1000
    p = []
    e= []
    T = 10

    # set particles
    for i in range(N):
        x = robot()
        x.set_noise(0.05, 0.05, 5.0)
        p.append(x)

    # move particles
    p2 = []
    for j in range(T):
        for i in range(N):
            p2.append(p[i].move(0.1, 5.0))
        p = p2

    # Particle Weight
        w = []
        for i in range(N):
            w.append(p[i].measurement_prob(Z))

    # resampling wheel
        p3 = []
        index = int(random.random() * N)
        beta = 0.0
        mw = max(w)
        for i in range(N):
            beta += random.random() * 2.0 * mw
            while beta > w[index]:
                beta -= w[index]
                index = (index + 1) % N
            p3.append(p[index])
        p = p3
        e.append(eval(myrobot, p))
    for i in e:
        print(i)

    # print('\n')
    # for i in p:
    #     print(i)
    # print("the real one\n", myrobot)


if __name__ == '__main__':
    main()
