import numpy as np
import random



def resample(particles, weights):
    N = len(particles)
    cumulativeProbability = np.zeros(N + 1)

    # Standard discrete sampling: stack the probabilities in the interval [0, 1]
    # Then choose a random number in the interval and select the particle
    # whose probability corresponds to that interval

    for i in range(1, N + 1):
        cumulativeProbability[i] = cumulativeProbability[i - 1] + weights[i - 1]

    newParticles = np.copy(particles)
    for i in range(N):
        number = random.uniform(0.0, cumulativeProbability[N])

        idx = np.searchsorted(cumulativeProbability, number) - 1

        newParticles[i, :] = particles[idx, :]
    return newParticles


def test():
    particles = np.array([
     [1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05],
     [2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05],
     [4.0, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1],
     [6.0, 7.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1],
     [8.0, 9.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25],
     [10.0, 11.0, 0.0, 0.0, 0.0, 0.0, 0.0,  0.45]
    ])
    weights = particles[:, 7]
    print(weights)
    print(len(particles))
    newParticles = resample(particles, weights)
    print(newParticles)

if __name__ == '__main__':
    test()
