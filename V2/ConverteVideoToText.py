import os
import argparse
import time
import numpy as np
import cv2


def convert_video_frames(path: str, target_fps: int):
    print(path)
    width: int = 400

    video_capture = cv2.VideoCapture(path)
    original_fps: float = video_capture.get(cv2.CAP_PROP_FPS)
    skip_frames: int = int(original_fps / target_fps)

    frame_count: int = 0
    while True:
        start_time = time.time()
        ret, frame = video_capture.read()

        if not ret:
            break

        if frame_count % skip_frames != 0:
            frame_count += 1
            continue

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height = int(gray_frame.shape[0] * (width / gray_frame.shape[1]))
        scaled_frame = cv2.resize(gray_frame, (width, height))

        frame: list[str] = convert_frame_to_ascii(scaled_frame, (height, width))
        display_frame(frame, start_time)

        frame_count += 1

    video_capture.release()


def convert_frame_to_ascii(image, dim: (int, int), chunk_size: int = 4) -> list[str]:
    frame: list[str] = []
    for y in range(0, dim[0], chunk_size*2):
        line = ""
        for x in range(0, dim[1], chunk_size):
            # Berechne den durchschnittlichen Helligkeitswert des Chunks
            chunk = image[y:y + chunk_size, x:x + chunk_size]
            if np.any(chunk):
                avg_brightness = int(chunk.mean())
            else:
                avg_brightness = 0

            # Wandele den Helligkeitswert in einen ASCII-Charakter um
            ascii_char = brightness_to_ascii(avg_brightness)
            line += ascii_char
        frame.append(line)

        # Beschränke die ASCII-Breite auf 80 Zeichen
    return frame


def brightness_to_ascii(brightness):
    ascii_chars = '@%#*+=-:. '
    index = int((brightness / 255) * (len(ascii_chars) - 1))
    return ascii_chars[index]


def display_frame(ascii_frame: list[str], start_time: float):
    for line in ascii_frame:
        print(line)

    execution_time = 0.2 - (time.time() - start_time)
    print(execution_time)
    print(f"\033[{len(ascii_frame)+1}A", end="")
    time.sleep(execution_time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Program to process a video.")
    parser.add_argument("--file", dest="file", help="Video file", required=True)
    parser.add_argument("--fps", dest="fps", help="target fps", required=False, default=5)
    args = parser.parse_args()

    main_path: str = args.file
    main_fps: int = args.fps

    if not os.path.exists(main_path):
        print("Invalid file name")
    else:
        convert_video_frames(os.path.join(os.curdir, main_path), main_fps)
