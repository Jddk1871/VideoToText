import cv2
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from sys import getsizeof
import math
import pickle
import os
from time import sleep
from time import time

import ProgressBar


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
    # __ = privat
    # _ = geschützt
    def __init__(self, path, fps):
        if fps <= 0:
            fps = 1
            print(bcolors.WARNING + "Warning: FPS below 0 --> set to 1" + bcolors.ENDC)
        self.__path = path
        self.__imPath = "Frames/" + str(self.__path.split('.')[-2]).split('/')[-1]
        print(self.__imPath)
        self.__fps = fps
        self.__vidFrames = []
        # self.__vidFrames1 = 0

    def VideoToImages(self, newVideoWidth=800):
        # newVideoWidth in pixeln
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
        framesToSkip = round(maxFrames / maxNewFrames)

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
        if not os.path.exists(self.__imPath):
            os.makedirs(self.__imPath)

        while (stream.isOpened()):
            print(end="\r" f"Current Frame: {currentFrame} von {maxFrames}")
            ret, frame = stream.read()

            # Wenn das Video zu ende ist , hört das ganze auf
            if frame is not None:
                if currentFrame % framesToSkip == 0 or currentFrame == 0:
                    # define the alpha and beta
                    # alpha = 1.5  # Contrast control
                    # beta = 1  # Brightness control
                    # call convertScaleAbs function
                    # frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

                    resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
                    greyFrame = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
                    # Speichert alle frames
                    cv2.imwrite(f"{self.__imPath}/{currentFrame}.jpg", greyFrame)
                    self.__vidFrames.append(greyFrame)

            else:
                stream.release()
                print(bcolors.UNDERLINE + f"\nFrames in List: {len(self.__vidFrames)}" + bcolors.ENDC)
                print("Finished reading video file\n+++")

                # print(f"Original Size: {getsizeof(self.__vidFrames)}")
                # self.__vidFrames1 = np.array(self.__vidFrames, np.int8)
                # print(f"Numpy Size: {getsizeof(self.__vidFrames1)}")

                break
            currentFrame += 1


class ImageToText:

    def __init__(self, path: str, skip: int, chunk: int):
        self.__path = path
        self.__savePath = "./saves/" + path.split('/')[-2]
        self.__frameCount = len(os.listdir(path))
        self.__skip = skip  # Für die FPS, bekommt man von VideoToImages framesToSkip
        self.__frameList = self.GetImages()
        self.__chunk_dim = chunk
        self.charSet = [' ', '.', '"', '/', '%']
        # self.charSet = [' ', '"', ',', '(', 'S', '#', '@']
        self.charFrameSet = []
        self.__globalCounter = 0

    def WriteCharFramesToFile(self):
        pBar = ProgressBar.ProgressBar(self.__frameCount, 50)
        print(bcolors.HEADER + "Convert Images to Char Images" + bcolors.ENDC)
        img_counter = 1
        for img in self.__frameList:
            pBar.progressBarMk2(img_counter)
            self.charFrameSet.append(self.pic_to_rgb(img))
            img_counter += 1
        print(bcolors.OKGREEN + "Convert: Complete" + bcolors.ENDC)

        with open(self.__savePath, "wb") as file:
            pickle.dump(self.charFrameSet, file)

    def Start(self):
        with open(self.__savePath, "rb") as file:
            self.charFrameSet = pickle.load(file)

        frameList = []

        for frame in self.charFrameSet:
            # sleep(.1)
            frame1 = ""
            for row in frame:
                # print(row)
                frame1 += f"{row}\n"
            frameList.append(frame1)

        clear = lambda: os.system('cls')
        for frame in frameList:
            # clear()
            print(frame, flush=True)
            sleep(.1)

    def GetImages(self):
        imgList = [cv2.imread(os.path.join(self.__path, f"{frame}.jpg"))
               for frame in range(0, self.__frameCount * self.__skip, self.__skip)]
        return imgList

    def pic_to_rgb(self, img: list) -> list:
        dim = self.__chunk_dim  # y, x print(img[599, 799])
        chunk_array = []

        for y in range(0, img.shape[0], dim * 2):  # range(x, y, z) z nimmt jeden (z)ten eintrag
            chunk_row = ""
            for x in range(0, img.shape[1], dim):
                chunk = img[y:y + dim, x:x + dim]
                row = chunk[0, :, 0] / dim + chunk[1, :, 0] / dim + chunk[2, :, 0] / dim + \
                      chunk[3, :, 0] / dim + chunk[4, :, 0] / dim  # Deswegen /(chunk größe) Wertebereich 2^8 rgb
                row_sum = round(sum(row) / dim)
                row_sum = max(1, math.ceil(row_sum / (255 / len(self.charSet))))
                chunk_row += self.charSet[row_sum - 1]
            chunk_array.append(chunk_row)
        return chunk_array


class ImageTester:

    def __init__(self):
        self.__testCharList = [' ', '"', ',', '#', '+', '*', '-', 'S', 'A', 'D', '.', 'ß', '?', '§', '$', '%',
                               'M', 'N', 'Y', '/', 'Q', 'q', 'a', 'c', 'o', '<', '>', '|']

    def TestPicturesChar(self):
        counter = 0
        for a in self.__testCharList:
            filename = f"dump/{counter}.png"
            fnt = ImageFont.truetype('arial.ttf', 20)

            image = Image.new(mode="RGB", size=(22, 35), color="black")

            draw = ImageDraw.Draw(image)
            draw.text((5, 5), a, font=fnt, fill=(204, 204, 204))

            image.save(filename)
            counter += 1
        print("Test images created")


if __name__ == '__main__':
    # vid = VideoCapture('media/BadApple.mp4', 5)
    # vid.VideoToImages()

    texter = ImageToText('./Frames/BadApple/', 6, 5)
    texter.WriteCharFramesToFile()
    texter.Start()
