import sys
import time


def progressbar(it, prefix="", size=60, out=sys.stdout):  # Python3.3+
    count = len(it)

    def show(j):
        x = int(size * j / count)
        print("{}[{}{}] {}/{}".format(prefix, "#" * x, "." * (size - x), j, count),
              end='\r', file=out, flush=True)

    show(0)
    for i, item in enumerate(it):
        yield item
        show(i + 1)
    print("\n", flush=True, file=out)


def progressBarMK2(steps, currentStep, barLenght):
    pro = round((currentStep / steps) * 10)
    rem = steps-pro
    print(end='\r' f"Progress: [{'#' * pro}{'.' * rem}]")


for i in range(0, 20):
    progressBarMK2(20, i, 20)
    time.sleep(.5)
