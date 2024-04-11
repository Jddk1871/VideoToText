import math
import time


class ProgressBar:

    def __init__(self, max_steps: int, bar_length: int):
        self.maxSteps = max_steps
        self.bar_length = bar_length
        self.bar_pro = self.bar_length / 100
        self.lastTime = time.time() - 0.1

    def progress_bar_mk2(self, increase: int):
        last_time = self.lastTime
        self.lastTime = time.time()
        time_delta = round(((last_time - self.lastTime) * -1), 2)

        if time_delta != 0:
            iops = round((1.0 / time_delta), 2)
        else:
            iops = None

        pro = math.floor((increase / self.maxSteps) * 100 * self.bar_pro)

        rem = self.bar_length - pro

        pref = "Progress"
        if increase == self.maxSteps:
            pref = "Complete"

        print(end='\r' f"{pref}: [{'#' * pro}{'.' * rem}] {increase}/{self.maxSteps}  {iops} IOPS/s ")
