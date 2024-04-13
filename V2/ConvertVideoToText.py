import os
import argparse
import time
import numpy as np
import cv2


def convert_video_frames(path: str, target_fps: int | None, char_line_width: int | None, chunk_size: int | None):
    video_capture = cv2.VideoCapture(path)
    original_fps: float = video_capture.get(cv2.CAP_PROP_FPS)

    target_fps = target_fps if target_fps is not None else original_fps
    char_line_width = char_line_width if char_line_width is not None else 100
    chunk_size = chunk_size if chunk_size is not None else 4

    width: int = char_line_width * chunk_size

    print("Target fps:", target_fps)
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

        frame_list: list[str] = convert_frame_to_ascii(scaled_frame, (height, width), chunk_size)
        display_frame(frame_list, start_time, target_fps)

        frame_count += 1

    video_capture.release()


def convert_frame_to_ascii(image, dim: (int, int), chunk_size: int) -> list[str]:
    frame: list[str] = []
    for y in range(0, dim[0], chunk_size*2):
        line = ""
        for x in range(0, dim[1], chunk_size):
            chunk = image[y:y + chunk_size, x:x + chunk_size]
            if np.any(chunk):
                avg_brightness = int(chunk.mean())
            else:
                avg_brightness = 0

            ascii_char = brightness_to_ascii(avg_brightness)
            line += ascii_char
        frame.append(line)
    return frame


def brightness_to_ascii(brightness):
    ascii_chars = '@%#*+=-:. '
    index = int((brightness / 255) * (len(ascii_chars) - 1))
    return ascii_chars[index]


def display_frame(ascii_frame: list[str], start_time: float, fps: int):
    global skipped_frames

    for line in ascii_frame:
        print(line)

    target_delay: float = 1 / fps
    execution_time = time.time() - start_time
    full_delay: float = target_delay - execution_time
    if full_delay < 0:
        full_delay = 0
        skipped_frames += 1

    print(f'\nCompute time: {execution_time:.4f} / {(execution_time / (target_delay / 100)):.2f}% | Target delay: '
          f'{target_delay:.4f} | Extra delay: {full_delay:.4f} | Skipped frames: {skipped_frames}     ')
    print(f"\033[{len(ascii_frame)+2}A", end="")
    time.sleep(full_delay)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Program to convert a video to ascii art.")
    parser.add_argument("--file", dest="file", help="Video file", required=True)
    parser.add_argument("--fps", dest="fps", help="target fps, must be lower than actual", required=False)
    parser.add_argument("--width", dest="width", help="target width in char len. "
                                                      "80: 1 line is 80 characters long", required=False)
    parser.add_argument("--chunk_size", dest="chunk_size", help="Chunk size", required=False)

    args = parser.parse_args()

    main_path: str = args.file
    main_fps: int | None = int(args.fps) if args.fps is not None else None
    main_width: int | None = int(args.width) if args.width is not None else None
    main_chunk_size: int | None = int(args.chunk_size) if args.chunk_size is not None else None

    # global vars
    skipped_frames: int = 0

    if not os.path.exists(main_path):
        print("Invalid file name")
    else:
        convert_video_frames(os.path.join(os.curdir, main_path), main_fps, main_width, main_chunk_size)
