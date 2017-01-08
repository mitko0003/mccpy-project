import cv2

KEYCODE_ESC = 27
KEYCODE_Q = ord('q')

FPS = 15
WINDOW_NAME = "MCCPY"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450
SELECTION_RECT_SIZE = 100
PARTICLE_RECT_SIZE = 50
COLOR_RANGES = 8

EVENT_QUIT = "quit"
EVENT_MOUSE_POS = "mouse_pos"
EVENT_MOUSE_CLICK = "lbd"
EVENT_STARTED_TRACKING = "track"
EVENT_INITIAL_LOCATION = "initial_loc"
Events = { 
        EVENT_QUIT: False, 
        EVENT_MOUSE_CLICK: False,
        EVENT_STARTED_TRACKING: False,
        EVENT_INITIAL_LOCATION: (0, 0),
        EVENT_MOUSE_POS: (0, 0)
        }

def handle_input(fps):
    key = cv2.waitKey(1000//fps) & 0xFF
    if key < 0:
        return
    if Events[EVENT_MOUSE_CLICK]:
        if not Events[EVENT_STARTED_TRACKING]:
            Events[EVENT_STARTED_TRACKING] = True
            Events[EVENT_INITIAL_LOCATION] = Events[EVENT_MOUSE_POS]
        Events[EVENT_MOUSE_CLICK] = False
    if key in [KEYCODE_ESC, KEYCODE_Q]: #  or cv2.getWindowProperty(WINDOW_NAME, 0) < 0
        Events[EVENT_QUIT] = True

def handle_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        Events[EVENT_MOUSE_CLICK] = True 
    if event == cv2.EVENT_MOUSEMOVE:
        Events[EVENT_MOUSE_POS] = (x, y)

def init():
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, WINDOW_WIDTH, WINDOW_HEIGHT)
    cv2.setMouseCallback(WINDOW_NAME, handle_mouse)

def quit():
    cv2.destroyAllWindows()

def camera_resolution(capture):
    resolution = (capture.get(cv2.CAP_PROP_FRAME_WIDTH), capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return resolution

def read_image(filename):
    return cv2.imread(filename, 1)

def start_video_capture(output_filename):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    return cv2.VideoWriter(output_filename, fourcc, 20.0, (640,480))

def save_frame(output, frame):
    output.write(frame)

def finish_video_capture(output):
    output.release()

def histogram(image, top_left, bottom_right):
    buckets = [0] * COLOR_RANGES
    for i in range(top_left[0], bottom_right[0]):
        for j in range(top_left[1], bottom_right[1]):
            bucket = 0
            for c in range(3):
                component_range = (image[i][j][c] + 1) // (256 // COLOR_RANGES)
                buckets += (COLOR_RANGES ** c) * component_range(component_range)
            buckets[bucket] += 1

test_image = "image.jpg"
video_filename = "output.avi"

# code to save video/image
init()
capture = cv2.VideoCapture(0)
# capture = cv2.VideoCapture(video_filename)
# output = start_video_capture(video_filename)
# camera_resolution(capture)


while(True):
    # Capture frame-by-frame
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)

    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.circle(frame, Events[EVENT_MOUSE_POS], 100, (0, 0, 255), 4, cv2.LINE_AA)
    if Events[EVENT_STARTED_TRACKING]:
        cv2.rectangle(frame, (Events[EVENT_INITIAL_LOCATION][0] - SELECTION_RECT_SIZE, Events[EVENT_INITIAL_LOCATION][1] - SELECTION_RECT_SIZE), (Events[EVENT_INITIAL_LOCATION][0] + SELECTION_RECT_SIZE, Events[EVENT_INITIAL_LOCATION][1] + SELECTION_RECT_SIZE), (0, 0, 255), 4) 
    # hist = cv2.calcHist([img], [0], None, [256], (0,256))
    # cv2.putText(frame, "test!",(50, 50),cv2.FONT_HERSHEY_COMPLEX_SMALL,.7,(0,0,255))

    # Display the resulting frame
    # save_frame(output, frame)
    cv2.imshow(WINDOW_NAME, frame)
    handle_input(FPS)
    if Events[EVENT_QUIT]:
        break


# When everything done, release the capture
# finish_video_capture(output)
capture.release()
quit()
