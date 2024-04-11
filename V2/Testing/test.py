import time
from random import randint

def write_table():
    for i in range(0, 100):
        print(randint(0, 100))
        time.sleep(1)
        print("\033[1A", end="")


write_table()