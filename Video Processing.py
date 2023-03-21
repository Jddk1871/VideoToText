import cv2
import ffmpeg
import os
from pathlib import Path
from time import sleep

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class VideoCapture:
    #__ = privat
    #_ = geschützt
    def __init__(self, path, fps):
        self.__path = path
        self.__fps = fps
        if self.__fps <= 0:
            self.__fps = 1
            print(bcolors.WARNING + "Warning: FPS below 0 --> set to 1" + bcolors.ENDC)
        self.__vidFrames = []

    def VideoToImages(self, newVideoWidth=800):
        #newVideoWidth in pixeln
        stream = cv2.VideoCapture(self.__path)
        currentFrame = 0
        maxFrames = stream.get(7)
        dimXalt = newVideoWidth
        dimYalt = (stream.get(4) / stream.get(3)) * dimXalt
        dim = (int(dimXalt), int(dimYalt))

        if self.__fps > stream.get(5):
            self.__fps = stream.get(5)
            print(bcolors.WARNING + f"Warning: FPS above Video file --> set to {stream.get(5)}" + bcolors.ENDC)

        maxNewFrames = round(1 / stream.get(5) * self.__fps * maxFrames)
        framesToScip  = round(maxFrames / maxNewFrames)

        print(bcolors.HEADER + "-----------------------------------------" + bcolors.ENDC)
        print(bcolors.HEADER + "Video Info              New Video Info" + bcolors.ENDC)
        print(bcolors.HEADER + f"- Width: {stream.get(3)}\t\t\t- Width: {dimXalt}" + bcolors.ENDC)
        print(bcolors.HEADER + f"- Height: {stream.get(4)}\t\t\t- Height: {dimYalt}" + bcolors.ENDC)
        print(bcolors.HEADER + f"- FPS: {stream.get(5)}\t\t\t- FPS: {self.__fps}" + bcolors.ENDC)
        print(bcolors.HEADER + f"- Frames: {maxFrames}\t\t- Frames:  {maxNewFrames - 1}" + bcolors.ENDC)
        print(bcolors.HEADER + "-----------------------------------------" + bcolors.ENDC)

        # Video abfangen und in einzelne frames aufteilen
        print("+++")
        print("Reading Video file (resize + grey scale + fps crop)")
        while (stream.isOpened()):
            print(end="\r" f"Current Frame: {currentFrame} von {maxFrames}")
            ret, frame = stream.read()

            # Wenn das Video zu ende ist , hört das ganze auf
            if frame is not None:
                if currentFrame % framesToScip == 0 or currentFrame == 0:
                    resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
                    greyFrame = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
                    #Speichert alle frames
                    #cv2.imwrite(f"dump/{current_frame}.jpg", grey_frame)
                    self.__vidFrames.append(greyFrame)

            else:
                stream.release()
                print("\nFinished reading video file\n+++")
                print(len(self.__vidFrames))
                break

            currentFrame += 1




if __name__ == '__main__':
    start = VideoCapture('media/testMovie.mp4', 5)
    start.VideoToImages()





