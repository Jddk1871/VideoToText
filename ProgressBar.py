import math
import time
import sys
#import curses
#from curses import wrapper
import multiprocessing as mp


class ProgressBar:
    d = 0
    def __init__(self, maxSteps: int, barLenght: int):
        self.__maxSteps = maxSteps
        self.__barLenght = barLenght
        self.__barPro = self.__barLenght / 100
        self.__lastTime = time.time() - 0.1

    def progressBarMk2(self, increase: int):
        lastTime = self.__lastTime
        self.__lastTime = time.time()
        timeDelta = round(((lastTime - self.__lastTime) * -1), 2)

        iops = round((1.0 / timeDelta), 2)
        pro = math.floor((increase / self.__maxSteps) * 100 * self.__barPro)

        rem = self.__barLenght - pro

        pref = "Progress"
        if increase == self.__maxSteps:
            pref = "Complete"

        print(end='\r' f"{pref}: [{'#' * pro}{'.' * rem}] {increase}/{self.__maxSteps}  {iops} IOPS/s ")

    #Python Curses <-- WICHTIG!!!!!
    '''def progressBarMk2(self, increase: list, chunks:int):
        proList = []
        incCounter = 0
        for inc in increase:
            pro = math.floor(((inc-(chunks*incCounter)) / chunks) * 100 * self.__barPro)
            rem = self.__barLenght - pro
            proList.append([pro, rem])
            incCounter += 1

        b = ""
        for x in proList:
            b += f"Loading: [{'#' * x[0]}{'.' * x[1]}] {x[0]}/{chunks}\n"


        sys.stdout.write('\r' + b)
        sys.stdout.flush()


        print(end="\r")'''

#print()
#progressBar = ProgressBar(300, 10)

#print("Hallo\nHallo\nHallo\nHallo")
#print("Test", end='\r')
#print(end='\r' + "Ho\nHo\nHo\nHo")

#a = 0
#for x in range (0,3):
#    a = a + 1
#    b = ("Loading" + "." * a + "test\ntest")
#    # \r prints a carriage return first, so `b` is printed on top of the previous line.
#    sys.stdout.write('\r'+b)
#    sys.stdout.flush()
#    time.sleep(0.5)
#print (a)

#def main(stdscr):
#    stdscr.clear()
#    stdscr.addstr(10, 10, "Hallo")
#    stdscr.refresh()
#    stdscr.getch()

#wrapper(main)

'''def t(a, x):
    for i in range(1, 1001, 1):
        pBar = ProgressBar(1000, 100)
        pBar.progressBarMk2(i)

        time.sleep(.05)

t(1, 1)'''



