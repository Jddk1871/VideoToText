import cv2
import ffmpeg
import os
from pathlib import Path
from time import sleep


class VideoCapture:
    #__ = privat
    #_ = geschützt
    def __init__(self, path):
        self.__path = path
        self.__vidFrames = []

    def VideoToImages(self, newVideoWidth=800):
        #newVideoWidth in pixeln
        stream = cv2.VideoCapture(self.__path)
        currentFrame = 0
        max_frames = stream.get(7)

        print("-----Video Info-----")
        print("Width: ", stream.get(3))
        print("Height: ", stream.get(4))
        print("FPS: ", stream.get(5))
        print("Frames: ", max_frames)
        print("--------------------")

        dimXalt = newVideoWidth
        dimYalt = (stream.get(4) / stream.get(3)) * dimXalt
        print(f"New Dimensions:\nx: {dimXalt}, y: {dimYalt}")
        dim = (int(dimXalt), int(dimYalt))

        # Video abfangen und in einzelne frames aufteilen
        print("Reading Video file")
        while (stream.isOpened()):
            print(end="\r" f"Current Frame: {currentFrame} von {max_frames}")
            currentFrame += 1
            ret, frame = stream.read()

            # Wenn das Video zu ende ist , hört das ganze auf
            if frame is not None:
                resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
                greyFrame = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
                #Speichert alle frames
                #cv2.imwrite(f"dump/{current_frame}.jpg", grey_frame)
                self.__vidFrames.append(greyFrame)

            else:
                stream.release()
                print("\nFinished reading video file")
                break



if __name__ == '__main__':
    start = VideoCapture('media/testMovie.mp4')
    start.VideoToImages()





