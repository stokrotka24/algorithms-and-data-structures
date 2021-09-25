import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from Config import *
from PriorityQueueConfig import *


def main():
    try:
        m = int(input())
        lines = []
        for i in range(m):
            lines.append(input())

    except ValueError:
        print("enter m - integral number of commands and then proper m of commands")
        sys.exit()

    queue = PriorityQueue(desc_compare)
    commands_no_args = {'empty': queue.empty, 'top': queue.top, 'pop': queue.pop, 'print': queue.print}
    commands_with_args = {'insert': queue.insert, 'priority': queue.priority}

    for line in lines:
        split = line.split(" ")
        if len(split) == 1:
            command_name = split[0]
            command = commands_no_args[command_name]
            command()
        if len(split) == 3:
            command_name = split[0]
            x = split[1]
            p = split[2]
            command = commands_with_args[command_name]
            command(int(x), int(p))


if __name__ == '__main__':
    main()
