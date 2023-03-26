import multiprocessing as mp
import os
import random
import math
import time

N = 500000000
N2 = 250000000
N4 = 125000000

def cube(x):
    return math.sqrt(x)

if __name__ == "__main__":
    # first way, using multiprocessing
    start_time = time.perf_counter()
    with mp.Pool() as pool:
      result = pool.map(cube, range(10, N4))
      result1 = pool.map(cube, range(10, N4))
      result2 = pool.map(cube, range(10, N4))
      result3 = pool.map(cube, range(10, N4))
    finish_time = time.perf_counter()
    print("Program finished in {} seconds - using multiprocessing 2".format(finish_time-start_time))
    print("---")
    start_time = time.perf_counter()
    with mp.Pool() as pool:
      result4 = pool.map(cube, range(10, N))
    finish_time = time.perf_counter()
    print("Program finished in {} seconds - using multiprocessing 1".format(finish_time-start_time))
