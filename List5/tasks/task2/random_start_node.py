import shutil
import sys
from random import randint


def main():
    try:
        input_file = sys.argv[sys.argv.index('--input') + 1]
    except ValueError:
        sys.stderr.write("usage: python3.8 random_start_node.py --input file_name (WITHOUT extension)\n")
        sys.exit()
    with open(input_file + '.txt') as f:
        n = int(f.readline())

    start_vertex = randint(0, n-1)
    output_file = input_file + '_' + str(start_vertex) + '.txt'
    shutil.copyfile(input_file + '.txt', output_file)

    graph_file = open(output_file, 'a')
    graph_file.write(str(start_vertex) + '\n')
    graph_file.close()


if __name__ == '__main__':
    main()