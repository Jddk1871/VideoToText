import cv2
import math
import pickle
import os
import ProgressBar
# import Menu
import prompt_toolkit
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
    def __init__(self, path_file: str, path_frames: str, fps: int):
        if fps <= 0:
            fps = 1  # Wenn die Bildfrequenz unter 0 liegt, wird sie auf 1 gesetzt
            print(bcolors.WARNING + "Warning: FPS below 0 --> set to 1" + bcolors.ENDC)
        # Setzen von Attributen für den Pfad zum Video,
        # den Pfad für die Bilder, die Bildfrequenz und eine Liste für die Frames
        self.video_path = path_file
        self.images_path = path_frames
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
        print(bcolors.WARNING + f"Frames to skip: {frames_to_skip} \n" + bcolors.ENDC)

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
        return [self.display_fps, frames_to_skip]


class ImageToText:
    def __init__(self, path: str, path_save: str, skip: int, chunk_dim: int):
        self.path = path
        self.save_path = path_save  # Save path
        self.frame_count = len(os.listdir(path))  # Anzahl der Bilder im Pfad
        self.skip = skip  # Für die FPS, bekommt man von VideoToImages framesToSkip
        self.frame_list = self.get_images()  # Liste aller Frames im Pfad
        self.chunk_dim = chunk_dim  # Die Pixel zu char dimensionen x*(x*2)
        self.char_set = [' ', '.', '"', '/', '(', '%']  # Der verwendete Zeichensatz
        self.char_frame_set = []  # Die Liste für die Charakter-Images

    def write_char_frames_to_file(self):
        print(f"Save file --> {self.save_path}")
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

    def get_images(self) -> list:
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


class Menu:
    def __init__(self):
        self.menu_items = ["Video Capture", "Create Savefile", "Play Savefile", "End Programm"]
        self.file_completer = ['file1.txt', 'file2.txt', 'file3.txt']

        self.media_content = []
        self.save_content = []
        self.frame_folder = []

        self.path_default_frames = './Frames'
        self.path_default_frames_add = True
        self.path_default_saves = './saves'
        self.path_default_media = './media'

    def load_config(self):
        print(bcolors.HEADER + "Load config file" + bcolors.ENDC)
        try:
            with open("config.conf", "r") as config:
                for line in config:
                    var = line.split('=')
                    if var[0] == "path_default_frames":
                        self.path_default_frames = var[1].replace("\n", "")
                    if var[0] == "path_default_saves":
                        self.path_default_saves = var[1].replace("\n", "")
                    if var[0] == "path_default_media":
                        self.path_default_media = var[1].replace("\n", "")
                    if var[0] == "path_default_frames_add":
                        self.path_default_frames_add = bool(var[1].replace("\n", ""))

            print(bcolors.OKGREEN + "Loading successful" + bcolors.ENDC)
        except Exception:
            print(bcolors.FAIL + "Cant find config file" + bcolors.ENDC)

        print(bcolors.HEADER + "Get folder info" + bcolors.ENDC)
        try:
            self.check_folder(self.path_default_saves)
            self.save_content = self.get_folder_content(self.path_default_saves)

            self.check_folder(self.path_default_media)
            self.media_content = self.get_folder_content(self.path_default_media)

            print(bcolors.OKGREEN + "indexing successful" + bcolors.ENDC)

        except Exception:
            print(bcolors.FAIL + "Cant get folder content" + bcolors.ENDC)

        print("\n")
        self.menu()

    def menu(self):
        end_parm = True
        while end_parm:
            print(bcolors.HEADER + "Menu:" + bcolors.ENDC)
            for a in range(0, len(self.menu_items)):
                print(bcolors.HEADER + f"{a + 1}. {self.menu_items[a]}" + bcolors.ENDC)
            option = self.get_path(items=self.menu_items, info="Option")
            if option == self.menu_items[0]:
                self.video_to_frames()
            elif option == self.menu_items[1]:
                self.create_savefile()
            elif option == self.menu_items[2]:
                print("Gibts auch noch nicht")
            elif option == self.menu_items[3]:
                end_parm = False
            else:
                clear()
                print("Falsche eingabe!")

    def get_path(self, info: str, items: list[str]) -> str:
        # Übergibt, liste mit auswahlmöglichkeiten
        file_path = prompt(info + ': ', completer=WordCompleter(items))
        return file_path

    def get_folder_content(self, folder_path: str) -> list:
        folder_list = os.listdir(folder_path)
        return folder_list

    def check_folder(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def create_save_metadata(self, info: list[int, int], name: str):
        print(f"{self.path_default_saves}/{name}.inf")
        with open(f"{self.path_default_saves}/{name}.inf", "wb") as save:
            pickle.dump(info, save)
        print("Save created")

    def read_metadata(self, name: str) -> list[int, int]:
        print(f"{self.path_default_saves}/{name}.inf")
        try:
            with open(f"{self.path_default_saves}/{name}.inf", "rb") as save:
                data = pickle.load(save)
            return data
        except Exception:
            print(bcolors.FAIL + f"Faild to load save: {self.path_default_saves}/{name}.inf" + bcolors.ENDC)
            return [0, 0]

    def video_to_frames(self):

        print(bcolors.HEADER + "Convert Video to frames" + bcolors.ENDC)
        # print(self.file_completer)
        path_file = self.get_path(items=self.media_content, info="Videodatei")
        fps = 0
        check = True
        while check:
            try:
                fps = int(input("FPS: "))
                check = False
            except ValueError:
                print(bcolors.FAIL + "Please input integer only..." + bcolors.ENDC)

        vid_path = os.path.join(os.path.join(self.path_default_media, path_file))

        frame_path = self.path_default_frames
        if self.path_default_frames_add:
            frame_path = os.path.join(frame_path, path_file.split('.')[0])

        self.check_folder(frame_path)

        print(vid_path)
        print(frame_path)
        vid = VideoCapture(path_file=vid_path,
                           path_frames=frame_path,
                           fps=int(fps))

        metadata = vid.VideoToImages()
        print("\n")
        self.create_save_metadata(info=metadata, name=path_file.split('.')[0])

        print("\n")
        input(bcolors.OKCYAN + "Press Enter to continue..." + bcolors.ENDC)
        clear()

    def create_savefile(self):
        print(bcolors.HEADER + "Create savefile from images" + bcolors.ENDC)
        folder = self.get_path(info="Select folder", items=self.get_folder_content(self.path_default_frames))
        folder_path = os.path.join(self.path_default_frames, folder)
        info = self.read_metadata(folder)
        if self.get_folder_content(folder_path) and info != [0, 0]:
            texter = ImageToText(folder_path, f"{self.path_default_saves}/{folder}.save", 6, 5)
            texter.write_char_frames_to_file()
        else:
            print(bcolors.FAIL + "Folder is empty" + bcolors.ENDC)
        print("\n")
        input(bcolors.OKCYAN + "Press Enter to continue..." + bcolors.ENDC)
        clear()


if __name__ == '__main__':
    player = Menu()
    player.load_config()
    # player.frames_to_save()

    # vid = VideoCapture('media/BadApple.mp4', 5)
    # vid.VideoToImages()

    # texter = ImageToText('./Frames/BadApple/', 6, 5)
    # texter.write_char_frames_to_file()
    # texter.start_playback()
