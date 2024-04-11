import os
import sys
import time


def typewriter(message):
    for char in message:

        sys.stdout.write('\033[0m')  # reset style to default
        sys.stdout.write(char)  # print char with default style
        sys.stdout.flush()

        if char not in ['\n', ' ']:
            for _ in range(3):
                sys.stdout.write('\b\033[47m\033[30m')  # move cursor back one space + highlight style
                sys.stdout.write(char)  # print char with highlight
                sys.stdout.flush()
                time.sleep(0.05)  # short pause to show the char with highlight

                sys.stdout.write('\b\033[0m')  # move cursor back + reset style to default
                sys.stdout.write(char)  # print char with default style
                sys.stdout.flush()
                time.sleep(0.1)  # pause before highlighting again

        else:
            if char == "\n":
                time.sleep(0.9)  # longer pause at new lines


os.system('cls' if os.name == 'nt' else 'clear')  # clear terminal screen before starting

message = "Hello! \n" \
          "We're glad to have you here! \n" \
          "How may I assist you? \n"

typewriter(message)  # execute the function
