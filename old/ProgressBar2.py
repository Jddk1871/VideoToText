import math
import time

class ProgressBar:
    def __init__(self, max_steps: int, bar_length: int):
        self.max_steps = max_steps
        self.bar_length = bar_length
        self.bar_proportion = bar_length / 100
        self.start_time = time.time()
        self.last_time = self.start_time

    def update(self, current_step: int):
        current_time = time.time()
        time_delta = current_time - self.last_time
        self.last_time = current_time

        #iops = round((1.0 / time_delta), 2)
        progress = math.floor((current_step / self.max_steps) * 100 * self.bar_proportion)

        remaining = self.bar_length - progress

        prefix = "Progress"
        if current_step == self.max_steps:
            prefix = "Complete"

        print(
            f"\r{prefix}: [{'#' * progress}{'.' * remaining}] {current_step}/{self.max_steps}  {1} IOPS/s",
            end=""
        )
