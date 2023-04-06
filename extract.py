#!/usr/bin/env python

import os
import sys
from mmap import mmap, ACCESS_READ


if len(sys.argv) < 2:
    print("DOH")
    sys.exit(1)

image_path = sys.argv[1]


def locate_video_google(data):
    signatures = [b'ftypmp42', b'ftypisom', b'ftypiso2']
    for signature in signatures:
        position = data.find(signature)
        if position != -1:
            return position - 4
    return -1


def locate_video_samsumg(data):
    signature = b"MotionPhoto_Data"
    position = data.find(signature)
    if position != -1:
        return position + len(signature)
    return -1


def extract_embedded_video(input_path, output_path):
    with open(input_path, "rb") as image:
        with mmap(image.fileno(), 0, access=ACCESS_READ) as mm:
            position = locate_video_google(mm) or locate_video_samsumg(mm)

            if position != -1:
                with open(output_path, "wb+") as video:
                    mm.seek(position)
                    data = mm.read(mm.size())
                    video.write(data)
                print(f"Video saved to {output_path}")
            else:
                print("No video found in the given image file.")


if __name__ == "__main__":
    video_path = os.path.splitext(image_path)[0] + ".mp4"
    extract_embedded_video(image_path, video_path)
