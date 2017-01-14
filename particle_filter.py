from opencv import *
from initParticles import initParticles
from update_estimate_adapt_utils import *
from resample import resample
from propagate import propagate
import numpy as np
import time
import math
#number of particles
N = 100
sigma = 0.1
alpha = 0.1


def get_particles_weights(particles, target):
    particle_histograms = []
    top_left, bottom_right = particle_center_to_particle_corners(target)
    target_hist = per_color_histogram(frame, top_left, bottom_right)
    # print(target_hist)
    for i in range(len(particles)):
        particle = particles[i]
        top_left, bottom_right = particle_center_to_particle_corners(particle)
        particle_histograms.append(per_color_histogram(frame, top_left, bottom_right))
    return get_weights(target_hist, particle_histograms, sigma)

def particle_center_to_particle_corners(particle):
    top_left = int(particle[0] - particle[4] // 2), int(particle[1] - particle[5] // 2)
    bottom_right = int(particle[0] + particle[4] // 2), int(particle[1] + particle[5] // 2)
    return top_left, bottom_right


target = None
init()
capture = cv2.VideoCapture(0)
particle_delta_limits = [200, 200, 0.1]
noise = [50,50,10,10,50,50,0.1];


while target is None:
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)

    if Events[EVENT_SELECTING]:
        top_left, bottom_right = create_rect(Events[EVENT_SELECTION_RECT][0], Events[EVENT_MOUSE_POS])
        cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 4)
    if Events[EVENT_STARTED_TRACKING]:
        cv2.rectangle(frame, Events[EVENT_SELECTION_RECT][0], Events[EVENT_SELECTION_RECT][1], (0, 0, 255), 4)

    cv2.imshow(WINDOW_NAME, frame)

    target = handle_input(FPS)
    if target is not None:
        center = np.add(top_left, bottom_right) / 2
        width = math.fabs(top_left[0] - bottom_right[0])
        height = math.fabs(top_left[1] - bottom_right[1])
        target_model = [center[0], center[1], 0, 0, width, height, 0]
        particles, weights = initParticles(target[0], target[1], N, particle_delta_limits)
        weights = get_particles_weights(particles, target_model)

    #TODO MAKE EVENT FOR MOUSE RELEASE INSTEAD OF THIS


while True:
    particles = resample(particles, weights)
    particles = propagate(particles, noise, (640, 480))
    # get frame
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)

    # draw all particles
    for particle in particles:
      top_left, bottom_right = particle_center_to_particle_corners(particle)
      cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 4)

    weights = get_particles_weights(particles, target_model)

    target_estimate = estimate(weights, particles)
    top_left, bottom_right = particle_center_to_particle_corners(target_estimate)
    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 4)

    handle_input(FPS)
    cv2.imshow(WINDOW_NAME, frame)
    if Events[EVENT_QUIT]:
      break

# When everything done, release the capture
# finish_video_capture(output)
capture.release()
quit()
