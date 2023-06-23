# Video_zu_Text
Video zu Text Konverter 


Python 3.11

## Setup

Repo clonen und Start_Projekt.bat ausführen, sollte den rest von sich aus machen. 
-> Es muss Python auf dem System installiert sein und in PATH, ansonsten in der .bat datei rein schreiben wo venv erstellt wird






Komponenten / Verlauf:

1. Ein Video nehmen und dieses Verkleinern / skalieren
    a. Das Video muss am besten in Schwarz weiß dargestellt werden und einen hohen kontrast aufweisen
    b. Das Video sollte größere Pbjekte im Fokus haben, damit das ganze besser dargestellt werden kann


1.5
    a. Allgemein die beste Methode finden um daten möglichst klein zu speichern, wenns ist kann das ganez auch gezipt werden
    b. kompression der Daten
    c. das ganze mit Multiprocessing machen, wegen performance und so
    d. SPEICHERN und Datenmanipulation mal schauen, pandas ?


2. Funktionen
    a. Das Video Skalieren
    b. Das Video zu schwarz weiß Konvertieren
    c. Den Kontrast des Videos erhöhen, sodass das ganze in der umwandlung gut sichtbar ist
    d. Die Framerat des Videos verringern und somit den speicher des ganzen minimieren
    e. Das Video in seine einzelnen Frames aufteilen
    f. eine mapping bethode finden, um bestimmten pixelbereichen im Video passende buchstaben und ahlen zu zu Ordnen
        I. Sämmtliche Zeichen erstellen und bestimmen was der helligkeits wert von ihnen im Rahmen von einer CMD Umgebung ist
           also wie hell der buchstbe A auf schwarzem Hintergrund ist usw.
        II. Aussuchen, wie viele helligkeiststufen das ganze Unterstützen soll und dem entsprechend die Zeichen auswählen
    g. Jeden Frame in Zonen unterteilen, denen ein Zeichen zugeordnet werden soll (vielleicht 5px5p oder so)
    h. Jeden Frame Speichern, zum speichern das ganze in 4bit blöcke oder so aufteilen, und so die werte der einzelnen zeichen zuweisen
       dient zum Komrimieren der Daten, muss eim encodieren halt angegeben werden
    i. Das ganze in eine Datei dumpen, am besten ohne Filesystem und die bytes oder was es werden wirklich schreiben. Um overhead zu vermeiden
    j. Nun das ganze wieder einlesen, encodieren und laden
    k. Den Datensatz an den entsprechenden stellen trennen (kp jeder frame startet mit nur nullern)
    (l). Entwerder die Frames encodieren und dann ausgeben oder on the fly. Mal schauen was mehr speicher und Leistung verbraucht
    m. Fertig



Code Infos:

ImageToText
           pic_to_rgb:
           # Chunk aufbau= y1: x1, x2, x3, x4, x5
           #               y2: x1, x2, x3, x4, x5
           #               y3: x1, x2, x3, x4, x5
           #               y4: x1, x2, x3, x4, x5
           #               y5: x1, x2, x3, x4, x5

           old:
           #row_sum = round(sum(row) / dim)
           #if row_sum == 0:
           #    row_sum = 0.1
           #value_r = math.ceil(row_sum / (255 / len(self.charSet)))
           #chunk_row += self.charSet[value_r - 1]




