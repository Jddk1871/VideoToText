import cv2
import ffmpeg
import os
from pathlib import Path
from time import sleep


class VideoCapture:

    def VideoToImages(path, newVideoWidth=800):
        stream = cv2.VideoCapture(path)
        current_frame = 0
        max_frames = stream.get(7)

        print("-----Video Info-----")
        print("Breite: ", stream.get(3))
        print("Höhe: ", stream.get(4))
        print("FPS: ", stream.get(5))
        print("Frames: ", max_frames)
        print("--------------------")

        dimX_alt = newVideoWidth
        dimY_alt = (stream.get(4) / stream.get(3)) * dimX_alt
        print(f"x: {dimX_alt}, y: {dimY_alt}")
        dim = (int(dimX_alt), int(dimY_alt))

        vid_frames = []

        # Video abfangen und in einzelne frames aufteilen
        print("Reading Video file")
        while (stream.isOpened()):
            print(end="\r" f"Current Frame: {current_frame} von {max_frames}")
            current_frame += 1
            ret, frame = stream.read()

            # Wenn das Video zu ende ist , hört das ganze auf
            if frame is not None:
                resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
                grey_frame = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(f"dump/{current_frame}.jpg", grey_frame)



            else:
                stream.release()
                break


if __name__ == '__main__':
    VideoCapture.VideoToImages('media/testMovie.mp4')

