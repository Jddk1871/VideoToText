from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.shortcuts import clear
import os

# Liste von Menüpunkten
menu_items = ["Option 1", "Option 2", "Datei auswählen", "Option 3"]

# Komplettierer für Dateipfade
file_completer = WordCompleter(['file1.txt', 'file2.txt', 'file3.txt'])
current_directory = 'E:/'

file_completer = PathCompleter(file_completer)
# Funktionen, die aufgerufen werden sollen
def func_option1():
    print("Option 1 ausgewählt")

def func_option2():
    print("Option 2 ausgewählt")

def func_option3():
    print("Option 3 ausgewählt")

def func_select_file():
    #  Auswahl aus einer erstellten Liste
    #file_path = prompt('Dateipfad: ', completer=file_completer)
    #   Auswahl aus Daten

    #test = prompt('Test: ')
    #print(test)

    file_path = prompt('Dateipfad: ', completer=file_completer)
    print(f"Ausgewählte Datei: {file_path}")


# Menü erstellen
menu_functions = [func_option1, func_option2, func_select_file, func_option3]
menu = [(f"{i+1}. {item}", menu_functions[i]) for i, item in enumerate(menu_items)]

# Prompt-Session starten und Menü anzeigen
session = PromptSession()

while True:
    clear()
    print("Menü:")
    for item in menu:
        print(item[0])

    selection = session.prompt("Auswahl: ")
    menu[int(selection) - 1][1]()