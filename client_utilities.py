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
    if in_frame is None:
        return in_frame
    out_frame = in_frame
    img_h, img_w, _ = out_frame.shape
    cv2.line(out_frame, (0, int(img_h / 4)),
             (img_w, int(img_h / 4)), (100, 100, 100), 1, 1)
    cv2.line(out_frame, (0, int(img_h / 4 * 3)),
             (int(img_w), int(img_h / 4 * 3)), (100, 100, 100), 1, 1)
    cv2.line(out_frame, (int(img_w / 4), 0),
             (int(img_w / 4), int(img_h)), (100, 100, 100), 1, 1)
    cv2.line(out_frame, (int(img_w / 4 * 3), 0),
             (int(img_w / 4 * 3), int(img_h)), (100, 100, 100), 1, 1)
    return out_frame


def get_frame(url: str, img_h: int, img_w: int, img_c: int) -> tuple:
    try:
        data = {"height": img_h, "width": img_w, "channels": img_c, "request_time": time.time_ns()}
        r = requests.get(url=url, params=data)
        returned_json = json.loads(r.content)
        original = base64.b64decode(returned_json["frame_string"])
        out_frame = decode_image(original, img_w, img_h, img_c)
        delay = time.time_ns() - int(returned_json["request_time"])
        return out_frame, delay
    except requests.exceptions.ConnectionError:
        return None, 0
