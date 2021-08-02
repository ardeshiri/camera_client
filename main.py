import cv2
import numpy
import time
import requests
import base64
import json


def decode_image(string_frame, w, h, ch):
    try:
        decoded = numpy.fromstring(string_frame, dtype=numpy.uint8)
        decoded = decoded.reshape((h, w, ch))
        return decoded
    except:
        return numpy.ndarray("")


def add_grid(in_frame):
    out_frame = in_frame
    cv2.line(out_frame, (0, int(img_h / 4)),
             (img_w, int(img_h / 4)), (100, 100, 100), 1, 1)
    cv2.line(out_frame, (0, int(img_h / 4 * 3)),
             (int(img_w), int(img_h / 4 * 3)), (100, 100, 100), 1, 1)

    cv2.line(out_frame, (int(img_w / 4), 0),
             (int(img_w / 4), int(img_h)), (100, 100, 100), 1, 1)
    cv2.line(out_frame, (int(img_w / 4 * 3), 0),
             (int(img_w / 4 * 3), int(img_h)), (100, 100, 100), 1, 1)
    return out_frame


def show_stream(URL: str, img_h: int, img_w: int, img_c: int):
    while True:
        try:
            data = {"height": img_h, "width": img_w, "channels": img_c, "request_time": time.time_ns()}

            r = requests.get(url=URL, params=data)
            returned_json = json.loads(r.content)
            original = base64.b64decode(returned_json["frame_string"])
            out = decode_image(original, img_w, img_h, img_c)

            font = cv2.FONT_HERSHEY_PLAIN
            bottom_left_corner = (5, 10)
            font_scale = 0.8
            font_color = (255, 255, 255)
            line_thickness = 1
            cv2.putText(out, URL, bottom_left_corner, font, font_scale, font_color, line_thickness)
            delay = time.time_ns() - int(returned_json["request_time"])
            bottom_left_corner = (5, 20)
            cv2.putText(out, "delay: "+str(round(delay/1000000))+" ms", bottom_left_corner, font, font_scale, font_color, line_thickness)
            out = add_grid(out)

            cv2.imshow(mat=out, winname="frontcam")
            time.sleep(0.03)
            cv2.waitKey(1)
        except requests.exceptions.ConnectionError:
            break


# URL = "http://192.168.1.4:5000/frontcam"
URL = "http://127.0.0.1:5000/frontcam"
img_h = 180
img_w = 320
img_c = 1
show_stream(URL, img_h, img_w, img_c)
