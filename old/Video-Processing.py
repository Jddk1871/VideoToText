import ProgressBar2
import os
import cv2
import math
import pickle
from time import time
from ProgressBar2 import ProgressBar

class ImageToText:
    def __init__(self, path: str, skip: int, chunk: int):
        self.__path = path
        self.__savePath = f"./saves/{path.split('/')[-2]}"
        self.__frameCount = len(os.listdir(path))
        self.__skip = skip  # Für die FPS, bekommt man von VideoToImages framesToSkip
        self.__frameList = self.get_images()
        self.__chunk_dim = chunk
        self.charSet = [' ', '.', '/', '%']
        self.charSet = [' ', '"', ',', '(', 'S', '#', '@']
        self.charFrameSet = []
        self.__globalCounter = 0

    def write_char_frames_to_file(self):
        first_time = time()

        pbar = ProgressBar(max_steps=self.__frameCount, bar_length=50)
        print(f"\033[1mConverting Images to Char Images\033[0m")

        for idx, img in enumerate(self.__frameList):
            pbar.update(idx+1)
            self.charFrameSet.append(self.pic_to_rgb(img))

        last_time = time()
        print(f"\nConversion Time: {last_time-first_time:.2f}s")
        print(f"\033[92mConversion Complete\033[0m")

        with open(self.__savePath, "wb") as file:
            pickle.dump(self.charFrameSet, file)

    def get_images(self):
        imgList = []
        for frame in range(0, self.__frameCount * self.__skip, self.__skip):
            img = cv2.imread(os.path.join(self.__path, f"{frame}.jpg"))
            imgList.append(img)
        return imgList

    def pic_to_rgb(self, img: list) -> list:
        dim = self.__chunk_dim
        chunk_array = []

        for y in range(0, img.shape[0], dim):
            chunk_row = ""
            for x in range(0, img.shape[1], dim):
                chunk = img[y:y + dim, x:x + dim]
                row = chunk[0, :, 0] / dim + chunk[1, :, 0] / dim + chunk[2, :, 0] / dim + \
                    chunk[3, :, 0] / dim + chunk[4, :, 0] / dim
                row_sum = sum(row) / dim
                row_sum = round(row_sum) if row_sum > 0 else 1
                chunk_row += (self.charSet[math.ceil(row_sum * len(self.charSet) / 255)-1])
            if y % 2 == 0:
                chunk_array.append(chunk_row)

        return chunk_array

if __name__ == '__main__':
    #vid = VideoCapture('media/BadApple.mp4', 5)
    #vid.VideoToImages()

    texter = ImageToText('../Frames/BadApple/', 6, 5)
    texter.write_char_frames_to_file()