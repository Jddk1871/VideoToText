import cv2
import math
import pickle
import os
import ProgressBar
import Menu
from time import sleep
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.shortcuts import clear

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
    def __init__(self, path: str, fps: int):
        if fps <= 0:
            fps = 1  # Wenn die Bildfrequenz unter 0 liegt, wird sie auf 1 gesetzt
            print(bcolors.WARNING + "Warning: FPS below 0 --> set to 1" + bcolors.ENDC)
        # Setzen von Attributen für den Pfad zum Video,
        # den Pfad für die Bilder, die Bildfrequenz und eine Liste für die Frames
        self.video_path = path
        self.images_path = "Frames/" + str(self.video_path.split('.')[-2]).split('/')[-1]
        self.display_fps = fps

    def VideoToImages(self, new_video_width=800):  # new_video_width in pixeln = neues Format
        # Funktion zum Extrahieren von Einzelbildern aus einem Video
        stream = cv2.VideoCapture(self.video_path)

        current_frame = 0
        max_frames = stream.get(7)
        dim_x_alt = new_video_width
        dim_y_alt = (stream.get(4) / stream.get(3)) * dim_x_alt
        dim = (int(dim_x_alt), int(dim_y_alt))

        pbar = ProgressBar.ProgressBar(max_frames, 50)

        # Wenn die angezeigte FPS höher sind als die des Videos, wird sie auf die des Videos gesetzt
        if self.display_fps > stream.get(5):
            self.display_fps = stream.get(5)
            print(bcolors.WARNING + f"Warning: FPS above Video file --> set to {stream.get(5)}" + bcolors.ENDC)

        # Anzahl der neuen Frames berechnen, die pro Sekunde angezeigt werden sollen
        max_new_frames = round(1 / stream.get(5) * self.display_fps * max_frames)
        frames_to_skip = round(max_frames / max_new_frames)

        # Anzeigen von Informationen zum Video und den neu generierten Frames
        print(bcolors.HEADER + "-----------------------------------------" + bcolors.ENDC)
        print(bcolors.HEADER + "Video Info              New Video Info" + bcolors.ENDC)
        print(bcolors.HEADER + f"- Width: {stream.get(3)}\t\t\t- Width: {dim_x_alt}" + bcolors.ENDC)
        print(bcolors.HEADER + f"- Height: {stream.get(4)}\t\t\t- Height: {dim_y_alt}" + bcolors.ENDC)
        print(bcolors.HEADER + f"- FPS: {stream.get(5)}  \t\t\t- FPS: {self.display_fps}" + bcolors.ENDC)
        print(bcolors.HEADER + f"- Frames: {max_frames}\t\t- Frames:  {max_new_frames - 1}" + bcolors.ENDC)
        print(bcolors.HEADER + "-----------------------------------------" + bcolors.ENDC)

        # Erstellen des Ordners für die extrahierten Bilder, falls dieser noch nicht existiert
        if not os.path.exists(self.images_path):
            os.makedirs(self.images_path)

        # Extrahieren von Frames aus dem Video
        while stream.isOpened():
            pbar.progress_bar_mk2(current_frame)
            ret, frame = stream.read()

            # Wenn ein frame None ist, soll das ganze aufhören
            if frame is not None:
                if current_frame % frames_to_skip == 0 or current_frame == 0:
                    '''define the alpha and beta
                    alpha = 1.5  # Contrast control
                    beta = 1  # Brightness control
                    call convertScaleAbs function
                    frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)'''

                    # Image resize
                    resized_image = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
                    # Greyscale Image
                    grey_frame_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
                    # Speichert alle frames
                    cv2.imwrite(f"{self.images_path}/{current_frame}.jpg", grey_frame_image)

            else:
                stream.release()
                break
            current_frame += 1


class ImageToText:
    def __init__(self, path: str, skip: int, chunk_dim: int):
        self.path = path
        self.save_path = "./saves/" + path.split('/')[-2]  # Erstellt den Pfad für die gespeicherten Images
        self.frame_count = len(os.listdir(path))  # Anzahl der Bilder im Pfad
        self.skip = skip  # Für die FPS, bekommt man von VideoToImages framesToSkip
        self.frame_list = self.get_images()  # Liste aller Frames im Pfad
        self.chunk_dim = chunk_dim  # Die Pixel zu char dimensionen x*(x*2)
        self.char_set = [' ', '.', '"', '/', '(', '%']  # Der verwendete Zeichensatz
        self.char_frame_set = []  # Die Liste für die Charakter-Images

    def write_char_frames_to_file(self):
        # Fortschrittsanzeige für das Konvertieren der Bilder
        pbar = ProgressBar.ProgressBar(self.frame_count, 50)
        print("\n" + bcolors.HEADER + "Convert Images to Char Images" + bcolors.ENDC)
        img_counter = 1
        for img in self.frame_list:
            pbar.progress_bar_mk2(img_counter)
            # Fügt das konvertierte Charakter-Image zur Liste hinzu
            self.char_frame_set.append(self.pic_to_rgb(img))
            img_counter += 1
        print("\n" + bcolors.OKGREEN + "Convert: Complete" + bcolors.ENDC)

        # Speichert die Charakter-Images in einer Datei (Binär)
        with open(self.save_path, "wb") as file:
            pickle.dump(self.char_frame_set, file)

    def start_playback(self):
        # Lädt die Charakter-Images aus der Datei
        with open(self.save_path, "rb") as file:
            self.char_frame_set = pickle.load(file)

        # Gibt die Charakter-Images als Text aus
        for frame in self.char_frame_set:
            for row in frame:
                print(row)
            sleep(.1)

    def get_images(self):
        img_list = []
        for frame in range(0, self.frame_count * self.skip, self.skip):
            # Lädt das Bild mit dem angegebenen Dateinamen aus dem Ordner
            img = cv2.imread(os.path.join(self.path, f"{frame}.jpg"))
            img_list.append(img)
        return img_list

    def pic_to_rgb(self, img: list) -> list:
        dim = self.chunk_dim  # y, x print(img[599, 799])
        chunk_array = []

        for y in range(0, img.shape[0], dim * 2):  # range(x, y, z) z nimmt jeden (z)ten eintrag
            chunk_row = ""
            for x in range(0, img.shape[1], dim):
                chunk = img[y:y + dim, x:x + dim]
                # Berechnet den Grauwert jedes Chunks
                row = chunk[0, :, 0] / dim + chunk[1, :, 0] / dim + chunk[2, :, 0] / dim + \
                      chunk[3, :, 0] / dim + chunk[4, :, 0] / dim  # Wertebereich 2^8 rgb: Deswegen /(chunk größe)
                row_sum = round(sum(row) / dim)  # Summe der RGB Werte geteilt durch anzahl im Zeichensatz
                row_sum = max(1, math.ceil(row_sum / (255 / len(self.char_set))))  # Zuweisen ser Zeichen
                chunk_row += self.char_set[row_sum - 1]
            chunk_array.append(chunk_row)
        return chunk_array  # Charakter-Images zurück gegeben


class Player:
    def __int__(self):
        menu_items = ["Video Capture", "Create Savefile", "Play Savefile"]
        WordCompleter(['file1.txt', 'file2.txt', 'file3.txt'])
        path_default_frames = 'Frames/'
        path_default_saves = 'saves/'

    def get_path(self, items: list[str]) -> str:
        # Übergibt, liste mit auswahlmöglichkeiten
        file_path = prompt('Dateipfad: ', completer=WordCompleter(items))
        print(f"Ausgewählte Datei: {file_path}")
        return file_path

    def frames_to_save(self):
        vid = VideoCapture()



if __name__ == '__main__':
    vid = VideoCapture('media/Uni.mp4', 5)
    vid.VideoToImages()

    texter = ImageToText('./Frames/Uni/', 6, 5)
    texter.write_char_frames_to_file()
    texter.start_playback()







