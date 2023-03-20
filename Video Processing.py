import cv2





class VideoCapture:
    def VideoToImages(path):
        capture = cv2.VideoCapture(path)

        print("Breite: ", capture.get(3))
        print("Höhe: ", capture.get(4))
        print("FPS: ", capture.get(5))





if __name__ == '__main__':
    VideoCapture.VideoToImages("../Video_zu_Text/media\\testMovie.mp4")