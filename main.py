import cv2
import client_utilities
import time




channels = 1
width = 400
height = 300
def RGB_GRAY(*args):
    global channels
    if channels == 1:
        channels = 3
    else:
        channels = 1

def zoom_in(*args):
    global width
    global height
    width = int(width * 1.2)
    height = int(height * 1.2)

def zoom_out(*args):
    global width
    global height
    width = int(width / 1.2)
    height = int(height / 1.2)

def reset(*args):
    global width
    global height
    width = 400
    height = 300

def quit(*args):
    exit(0)

#URL = "http://192.168.1.4:5000/frontcam"
URL = "http://127.0.0.1:8080/frontcam"
cv2.namedWindow("w1")
cv2.createButton("color/gray", RGB_GRAY, None, cv2.QT_PUSH_BUTTON, 1)
cv2.createButton("zoom in", zoom_in, None, cv2.QT_PUSH_BUTTON, 1)
cv2.createButton("zoom out", zoom_out, None, cv2.QT_PUSH_BUTTON, 1)
cv2.createButton("reset", reset, None, cv2.QT_PUSH_BUTTON, 1)
cv2.createButton("close", quit, None, cv2.QT_PUSH_BUTTON, 1)

while True:
    f1, d1 = client_utilities.get_frame(URL, height, width, channels)
    font = cv2.FONT_HERSHEY_PLAIN
    bottom_left_corner = (5, 10)
    font_scale = 0.8
    font_color = (255, 255, 255)
    line_thickness = 1
    cv2.putText(f1, URL, bottom_left_corner, font, font_scale, font_color, line_thickness)
    bottom_left_corner = (5, 20)
    cv2.putText(f1, "delay: "+str(round(d1/1000000))+" ms", bottom_left_corner, font, font_scale, font_color, line_thickness)
    out = client_utilities.add_grid(f1)
    if f1 is not None:
        cv2.imshow(mat=f1, winname="w1")
    else:
        break
    time.sleep(.04)
    cv2.waitKey(1)

