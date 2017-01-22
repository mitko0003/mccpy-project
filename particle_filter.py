from opencv import *
from initParticles import initParticles
from update_estimate_adapt_utils import *
from resample import resample
from propagate import propagate
import numpy as np
import time
import math
import copy
#number of particles
WEBCAM = "webcam"
VIDEO = "video"
VIDEO_FILE_NAME = ""

CAPTURE_FROM = WEBCAM

N = 100
sigma = 0.1
alpha = 0.1


def get_particles_weights(frame, particles, target_hist):
    particle_histograms = []
    for i in range(len(particles)):
        particle = particles[i]
        top_left, bottom_right = particle_center_to_particle_corners(particle)
        particle_histograms.append(per_color_histogram(frame, top_left, bottom_right))
    return get_weights(target_hist, particle_histograms, sigma)

def particle_center_to_particle_corners(particle):
    top_left = int(particle[0] - particle[4] // 2), int(particle[1] - particle[5] // 2)
    bottom_right = int(particle[0] + particle[4] // 2), int(particle[1] + particle[5] // 2)
    return top_left, bottom_right

def init_target(frame):
    frame_copy = copy.deepcopy(frame)
    if Events[EVENT_SELECTING]:
        top_left, bottom_right = create_rect(Events[EVENT_SELECTION_RECT][0], Events[EVENT_MOUSE_POS])
        cv2.rectangle(frame_copy, top_left, bottom_right, (0, 0, 255), 2)
    if Events[EVENT_STARTED_TRACKING]:
        cv2.rectangle(frame_copy, Events[EVENT_SELECTION_RECT][0], Events[EVENT_SELECTION_RECT][1], (0, 0, 255), 4)

    cv2.imshow(WINDOW_NAME, frame_copy)
    target = handle_input(FPS)
    if target is not None:
        center = np.add(top_left, bottom_right) / 2
        width = math.fabs(top_left[0] - bottom_right[0])
        height = math.fabs(top_left[1] - bottom_right[1])
        target_model = [center[0], center[1], 0, 0, width, height, 0]
        particles, weights = initParticles(target[0], target[1], N, particle_delta_limits)
        top_left, bottom_right = particle_center_to_particle_corners(target_model)
        target_hist = per_color_histogram(frame, top_left, bottom_right)
        weights = get_particles_weights(frame, particles, target_hist)
        return target, target_model, target_hist, weights, particles


target = None
init()

if CAPTURE_FROM == WEBCAM:
    capture = cv2.VideoCapture(0)
else:
    capture = cv2.VideoCapture(VIDEO_FILE_NAME)

fps = int(capture.get(cv2.CAP_PROP_FPS))
# print(fps)
s_per_frame = 1 / fps
width = int(capture.get(3))
height = int(capture.get(4))

particle_delta_limits = [200, 200, 0.1]
noise = [50,50,10,10,50,50,0.1];

if CAPTURE_FROM == WEBCAM:
    while target is None:
        ret, frame = capture.read()
        frame = cv2.flip(frame, 1)
        init_t = init_target(frame)
        if init_t is not None:
            target, target_model, target_hist, weights, particles = init_t
        #TODO MAKE EVENT FOR MOUSE RELEASE INSTEAD OF THIS
else:
    ret, frame = capture.read()
    while target is None:
        init_t = init_target(frame)
        if init_t is not None:
            target, target_model, target_hist, weights, particles = init_t
            print(target_model[4] * target_model[5])


while True:
    start = time.time()
    particles = resample(particles, weights)
    particles = propagate(particles, noise, (width, height), Events[EVENT_RANDOM_GENERATOR])
    # get frame
    ret, frame = capture.read()
    if CAPTURE_FROM == WEBCAM:
        frame = cv2.flip(frame, 1)

    # draw all particles
    frame_copy = copy.deepcopy(frame)
    for particle in particles:
      top_left, bottom_right = particle_center_to_particle_corners(particle)
      cv2.rectangle(frame_copy, top_left, bottom_right, (0, 0, 255), 1)

    weights = get_particles_weights(frame, particles, target_hist)

    target_estimate = estimate(weights, particles)

    top_left, bottom_right = particle_center_to_particle_corners(target_estimate)
    cv2.rectangle(frame_copy, top_left, bottom_right, (0, 255, 0), 4)

    handle_input(fps)
    cv2.imshow(WINDOW_NAME, frame_copy)


    end = time.time()
    time_elapsed = end - start
    time_left_to_wait = s_per_frame - time_elapsed
    if time_left_to_wait > 0 and CAPTURE_FROM == VIDEO:
        cv2.waitKey(int(time_left_to_wait))
    if Events[EVENT_QUIT]:
      break

# When everything done, release the capture
# finish_video_capture(output)
capture.release()
quit()
