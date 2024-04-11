# Video-Ascii-Art-Converter

Dieses Python-Skript liest ein Video ein und wandelt jedes Frame in ASCII um, bevor es auf der Konsole ausgegeben wird. 
<br/> Es bietet die Möglichkeit, die Framerate des Ausgabevideos anzupassen.

## Install 
1. Python Version 3.12, sollte aber auch mit niedrigern gehen >3.8. 
2. Requirements.txt installieren

## Verwendung 
Führen Sie das Skript aus und geben Sie den Pfad zur Videodatei an, die Sie verarbeiten möchten, sowie die Ziel-Framerate (optional).
````
py ConvertVideoToText.py --file video.mp4 --fps
````

## Optionen
- `--file`: Pfad zur Videodatei, die verarbeitet werden soll. (Erforderlich)
- `--fps`: Ziel-Framerate des Ausgabevideos. Muss niedriger sein als die tatsächliche Framerate des Eingabevideos. (Optional)

