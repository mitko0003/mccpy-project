import cv2
import numpy as np


KEYCODE_ESC = 27
KEYCODE_Q = ord('q')

FPS = 15
WINDOW_NAME = "MCCPY"
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
PARTICLE_RECT_SIZE = 50
COLOR_RANGES = 8

EVENT_QUIT = "quit"
EVENT_MOUSE_POS = "mouse_pos"
EVENT_LMOUSE_DOWN = "lbd"
EVENT_LMOUSE_UP = "lbu"
EVENT_STARTED_TRACKING = "track"
EVENT_SELECTION_RECT = "sel_rec"
EVENT_SELECTING = "selecting"
EVENT_RANDOM_GENERATOR = "random"
Events = {
        EVENT_QUIT: False,
        EVENT_LMOUSE_DOWN: False,
        EVENT_LMOUSE_UP: False,
        EVENT_STARTED_TRACKING: False,
        EVENT_SELECTING: False,
        EVENT_SELECTION_RECT: [(0, 0), (0, 0)],
        EVENT_MOUSE_POS: (0, 0),
        EVENT_RANDOM_GENERATOR: "numpy"
        }

def create_rect(v1, v2):
    #print(v1, v2)
    return [(min(v1[0], v2[0]), min(v1[1], v2[1])), (max(v1[0], v2[0]), max(v1[1], v2[1]))]

def handle_input(fps):
    key = cv2.waitKey(1000//fps) & 0xFF
    if key < 0:
        return
    if Events[EVENT_LMOUSE_DOWN]:
        if not Events[EVENT_STARTED_TRACKING]:
            Events[EVENT_SELECTION_RECT][0] = Events[EVENT_MOUSE_POS]
            Events[EVENT_SELECTING] = True
        Events[EVENT_LMOUSE_DOWN] = False
    if Events[EVENT_LMOUSE_UP]:
        if not Events[EVENT_STARTED_TRACKING]:
            Events[EVENT_SELECTING] = False
            Events[EVENT_STARTED_TRACKING] = True
            Events[EVENT_SELECTION_RECT] = create_rect(Events[EVENT_SELECTION_RECT][0], Events[EVENT_MOUSE_POS])
        Events[EVENT_LMOUSE_UP] = False
        return Events[EVENT_SELECTION_RECT]
    if key in [KEYCODE_ESC, KEYCODE_Q]: #  or cv2.getWindowProperty(WINDOW_NAME, 0) < 0
        Events[EVENT_QUIT] = True

def handle_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        Events[EVENT_LMOUSE_DOWN] = True
    if event == cv2.EVENT_LBUTTONUP:
        Events[EVENT_LMOUSE_UP] = True
    if event == cv2.EVENT_MOUSEMOVE:
        Events[EVENT_MOUSE_POS] = (x, y)

def init():
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, WINDOW_WIDTH, WINDOW_HEIGHT)
    cv2.setMouseCallback(WINDOW_NAME, handle_mouse)
    switch = """\
            0 : numpy
            1 : sobol
            2 : faure
            3 : halton
            4 : niederreiter2
            """
    cv2.createTrackbar(switch,WINDOW_NAME,0,4,trackbar_handler)

def quit():
    cv2.destroyAllWindows()

def camera_resolution(capture):
    resolution = (capture.get(cv2.CAP_PROP_FRAME_WIDTH), capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return resolution

def read_image(filename):
    return cv2.imread(filename, 1)

def trackbar_handler(value):
    random_generators = {0: 'numpy', 1: 'sobol', 2: 'faure', 3: 'halton', 4: 'niederreiter2'}
    Events[EVENT_RANDOM_GENERATOR] = random_generators[value]

def start_video_capture(output_filename):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    return cv2.VideoWriter(output_filename, fourcc, 20.0, (640,480))

def save_frame(output, frame):
    output.write(frame)

def finish_video_capture(output):
    output.release()

def per_color_histogram(frame, top_left, bottom_right):
    particle = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    blue = cv2.calcHist([particle], [0], None, [8], [0,256])
    green = cv2.calcHist([particle], [1], None, [8], [0,256])
    red = cv2.calcHist([particle], [2], None, [8], [0,256])
    colors = [blue, green, red]
    for i in range(3):
        s = sum(colors[i])
        if s != 0:
            colors[i] /= s
    return np.array(colors)

def histogram(image, top_left, bottom_right):
    # print(len(image), len(image[0]))
    buckets = np.zeros(COLOR_RANGES ** 3)

    top_left = (max(top_left[0], 0), max(top_left[1], 0))
    bottom_right = (min(bottom_right[0], len(image) - 1), min(bottom_right[1], len(image[0] - 1)))

    for i in range(top_left[0], bottom_right[0]):
        for j in range(top_left[1], bottom_right[1]):
            bucket = 0
            for c in range(3):
                component_range = (image[i][j][c]) // (256 // COLOR_RANGES)
                bucket += (COLOR_RANGES ** c) * component_range
            buckets[bucket] += 1
    return np.divide(buckets, np.sum(buckets))

test_image = "image.jpg"
video_filename = "output.avi"

def capture_frame_actual(capture):
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)
    return frame

def show_frame(frame):
    cv2.imshow(WINDOW_NAME, frame)

def capture_frame(capture):
    # Capture frame-by-frame
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)

    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.circle(frame, Events[EVENT_MOUSE_POS], 100, (0, 0, 255), 4, cv2.LINE_AA)
    if Events[EVENT_SELECTING]:
        top_left, bottom_right = create_rect(Events[EVENT_SELECTION_RECT][0], Events[EVENT_MOUSE_POS])
        cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 4)
    if Events[EVENT_STARTED_TRACKING]:
        cv2.rectangle(frame, Events[EVENT_SELECTION_RECT][0], Events[EVENT_SELECTION_RECT][1], (0, 0, 255), 4)

    # hist = cv2.calcHist([img], [0], None, [256], (0,256))
    # cv2.putText(frame, "test!",(50, 50),cv2.FONT_HERSHEY_COMPLEX_SMALL,.7,(0,0,255))

    # Display the resulting frame
    # save_frame(output, frame)

    cv2.imshow(WINDOW_NAME, frame)
    handle_input(FPS)



# code to save video/image
def main_loop():
    init()
    capture = cv2.VideoCapture(0)
    # capture = cv2.VideoCapture(video_filename)
    # output = start_video_capture(video_filename)
    # camera_resolution(capture)
    used_to_select = False
    while(True):
        capture_frame(capture)

    # When everything done, release the capture
    # finish_video_capture(output)
        if Events[EVENT_QUIT]:
            break
    capture.release()
    quit()

# if __name__ == "__main__":
#     main_loop()
