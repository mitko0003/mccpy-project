import numpy as np
import math


def initParticles(upperLeft, lowerRight, N, limits):

    center = np.add(upperLeft, lowerRight) / 2
    # print(center)
    width = math.fabs(upperLeft[0] - lowerRight[0])
    height = math.fabs(upperLeft[1] - lowerRight[1])

    max_dx = min(limits[0], width/2)
    max_dy = min(limits[1], height/2)
    max_dsc = limits[2]

    particles = np.zeros((N, 7))
    weights = np.full(N, 1.0/N)

    delta = np.zeros(2)
    pos = np.zeros(2)

    for i in range(N):
        # Generate offset and scale change
        delta[0] = np.random.randint(0, max_dx + 1)
        delta[1] = np.random.randint(0, max_dy + 1)
        delta_sc = np.random.uniform(-max_dsc, max_dsc)

        # Calculate absolute position based on offset
        pos = np.add(center, delta)

        # Calculate new size based on scale change
        Hx = width * (1 + delta_sc)
        Hy = height * (1 + delta_sc)

        # Generate particle and round integer elements - number of pixels
        particle = [pos[0], pos[1], delta[0], delta[1], Hx, Hy, delta_sc]
        particle[0:6] = np.round(particle[0:6])
        print(type(particle[0]))
        particles[i,:] = particle[:]

    return particles, weights


def test():
    upperLeft = [0, 100]
    lowerRight = [100, 0]
    N = 10
    limits = [20, 20, 0.1]

    particles, weights = initParticles(upperLeft, lowerRight, N, limits)

    print(weights)
    print(particles)


if __name__ == "__main__":
    test()
