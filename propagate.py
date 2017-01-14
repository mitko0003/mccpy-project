import numpy as np
import math
import random

# Some global bounds
vmax = 10
minHeight = 50
maxHeight = 200
maxScaleChange = 0.1

# variances - the variances of the noise per dimension
# imageSize - width and height of image, should not go out of these bounds
def propagate(particles, variances, imageSize):
    N = len(particles)

    A = np.array([
        [1, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1]
    ])

    for i in range(N):
        #Take scale into consideration
        A[4,4] = 1 + particles[i, 6]
        A[5,5] = 1 + particles[i, 6]

        # Update according to the model:
        # First multiply by matrix
        # Then add random noise with expectation 0 and deviations, taken from the variance vectors
        # Here we use that (x - exp)/sqrt(deviation) ~ N(0, 1) for x ~ N(exp, deviation)

        # particles[i, :] = A.dot(np.transpose(particles[i, :])) + np.random.normal(0.0, 1.0, 7) * np.sqrt(variances)

        particles[i, :] = A.dot(particles[i, :]) + np.random.normal(0.0, 1.0, 7) * np.sqrt(variances)

        # Afterwards we can enforce some bounds

        # Coordinates, velocity and dimensions should be integers - number of pixels
        particles[i,0:6] = np.around(particles[i, 0:6])

        # First make sure particle remains in actual image
        particles[i,0] = np.clip(particles[i, 0], 0, imageSize[0])
        particles[i,1] = np.clip(particles[i, 1], 0, imageSize[1])

        # Then we can put bounds on velocity
        particles[i, 2:4] = np.clip(particles[i,2:4], -vmax, vmax)

        # Bounds on height
        particles[i, 4:6] = np.clip(particles[i,4:6], minHeight, maxHeight)

        # Bounds on scale
        particles[i, 6] = np.clip(particles[i,6], -maxScaleChange, maxScaleChange)

    return particles

def test():
    particles = np.array([
        [1.0, 2.0, 1.0, 1.0, 5.0, 5.0, 0.01],
        [2.0, 3.0, 1.0, -1.0, 5.0, 5.0, 0.01],
        [4.0, 5.0, -1.0, 1.0, 5.0, 5.0, 0.01],
        [6.0, 7.0, -1.0, 2.0, 5.0, 5.0, 0.01],
        [8.0, 9.0, 1.0, 0.0, 5.0, 5.0, 0.01],
        [10.0, 11.0, 0.0, 1.0, 5.0, 5.0, 0.01]
    ])

    variances = np.array([5, 5, 5, 5, 5, 5, 0.001])

    particles = propagate(particles, variances, {"width": 300, "height": 300})
    print(particles)

if __name__ == "__main__":
    test()
