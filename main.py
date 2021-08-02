import cv2
import numpy
import time
import requests
import base64
import json


def decodeImage(string_frame, w, h, ch):
    try:
        decoded = numpy.fromstring(string_frame, dtype=numpy.uint8)
        decoded = decoded.reshape((h, w, ch))
        return decoded
    except:
        return numpy.ndarray("")

#URL = "http://192.168.1.4:5000/frontcam"
URL = "http://127.0.0.1:5000/frontcam"

img_h = 180
img_w = 320
img_c = 1

while True:
    try:
        data = {"height": img_h, "width": img_w, "channels": img_c, "request_time": time.time_ns()}

        r = requests.get(url=URL, params=data)
        returned_json = json.loads(r.content)
        original = base64.b64decode(returned_json["frame_string"])
        out = decodeImage(original, img_w, img_h, img_c)
        #print(time.time_ns()-int(returned_json["request_time"]), "nanosec")
        font = cv2.FONT_HERSHEY_PLAIN
        bottomLeftCornerOfText = (5, 10)
        fontScale = 0.8
        fontColor = (255, 255, 255)
        lineThickness = 1
        cv2.putText(out, 'Frontcam', bottomLeftCornerOfText, font, fontScale, fontColor, lineThickness)
        cv2.line(out, (0, int(img_h / 4)),
                 (img_w, int(img_h / 4)), (100, 100, 100), 1, 1)
        cv2.line(out, (0, int(img_h/ 4 * 3)),
                 (int(img_w), int(img_h/ 4 * 3)), (100, 100, 100), 1, 1)

        cv2.line(out, (int(img_w/ 4), 0),
                 (int(img_w/ 4), int(img_h)), (100, 100, 100), 1, 1)
        cv2.line(out, (int(img_w / 4 * 3), 0),
                 (int(img_w / 4 * 3), int(img_h)), (100, 100, 100), 1, 1)

        cv2.imshow(mat=out, winname="frontcam")
        time.sleep(0.05)
        cv2.waitKey(1)
    except requests.exceptions.ConnectionError:
        break

