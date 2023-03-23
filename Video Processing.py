import cv2
import multiprocessing as mp
from PIL import Image, ImageDraw, ImageFont
from numpy.linalg import norm
import numpy as np
from sys import getsizeof



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
        if fps <= 0:
            fps = 1
            print(bcolors.WARNING + "Warning: FPS below 0 --> set to 1" + bcolors.ENDC)
        self.__path = path
        self.__fps = fps
        self.__vidFrames = []
        #self.__vidFrames1 = 0

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
        framesToSkip  = round(maxFrames / maxNewFrames)

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
                if currentFrame % framesToSkip == 0 or currentFrame == 0:

                    # define the alpha and beta
                    #alpha = 1.5  # Contrast control
                    #beta = 1  # Brightness control
                    # call convertScaleAbs function
                    #frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

                    resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
                    greyFrame = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
                    #Speichert alle frames
                    cv2.imwrite(f"BadApple/{currentFrame}.jpg", greyFrame)
                    self.__vidFrames.append(greyFrame)

            else:
                stream.release()
                print(bcolors.UNDERLINE + f"\nFrames in List: {len(self.__vidFrames)}" + bcolors.ENDC)
                print("Finished reading video file\n+++")


                #print(f"Original Size: {getsizeof(self.__vidFrames)}")
                #self.__vidFrames1 = np.array(self.__vidFrames, np.int8)
                #print(f"Numpy Size: {getsizeof(self.__vidFrames1)}")



                break

            currentFrame += 1


class ImageToText:

    def __init__(self, path, skip, chunk):
        self.__path = path
        self.__frameCount = len(os.listdir(path))
        print(f"Frames: {self.__frameCount}")
        self.__frameList = []
        self.__skip = skip # Für die FPS, bekommt man von VideoToImages framesToSkip
        self.__chunk_dim = chunk

    def GetImages(self):
        for frame in range(0, self.__frameCount*self.__skip):
            if frame % self.__skip == 0 or frame == 0:
                #print(frame)
                img = cv2.imread(os.path.join(self.__path, f"{frame}.jpg"))
                self.__frameList.append(img)
        print(len(self.__frameList))





    def PicToRGB(self):


        charSet = [' ', '.', '/', '%']
        img = cv2.imread(os.path.join(self.__path, f"{54}.jpg"))
        dim = self.__chunk_dim
        #y, x
        #print(img[599, 799])

        chunk_array = []
        for y in range(0, img.shape[0]):
            if y % dim == 0 or y == 0:
                chunk_row = []
                for x in range(0, img.shape[1]):
                    if x % dim == 0 or x == 0:
                        #Chunk aufbau= y1: x1, x2, x3, x4, x5
                        #              y2: x1, x2, x3, x4, x5
                        #              y3: x1, x2, x3, x4, x5
                        #              y4: x1, x2, x3, x4, x5
                        #              y5: x1, x2, x3, x4, x5
                        chunk = img[y:y+dim, x:x+dim]

                        #Bei der Addition ist zu beachten, das der Wertebereich 2^8 (rgb Wertebereich) deswegen /(chunk größe)
                        row = chunk[0, :, 0]/dim + chunk[1, :, 0]/dim + chunk[2, :, 0]/dim + \
                              chunk[3, :, 0]/dim + chunk[4, :, 0]/dim
                        #print(row)
                        row_sum = 0
                        for rgb in row:
                            row_sum += rgb
                        row_sum = round(row_sum / dim)
                        #print(row_sum)
                        chunk_row.append(row_sum)
                chunk_array.append(chunk_row)

        for row in chunk_array:
            print(row)













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

print()



if __name__ == '__main__':
    #start = VideoCapture('media/BadApple.mp4', 5)
    #start.VideoToImages()
    #imager = ImageTester()
    #imager.TestPicturesChar()

    texter = ImageToText('./BadApple/', 6, 5)
    texter.PicToRGB()






