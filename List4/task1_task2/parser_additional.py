import numpy as np
import shelve


def main():
    tree_types = ['bst', 'rbt', 'splay']
    operations = ['insert']

    for tree_type in tree_types:
        for operation in operations:
            time_file = 'results_additional/' + tree_type + '_' + operation
            with open(time_file + '.txt') as f:
                lines = [float(line.rstrip()) for line in f]

            x = []
            avgs = []
            i = 0
            for n in range(100, 10001, 100):
                x = np.append(x, n)
                avgs = np.append(avgs, lines[i])
                i = i + 1

            shelf_file = shelve.open('parsed_' + time_file)
            shelf_file['x'] = x
            shelf_file['avgs'] = avgs
            shelf_file.close()


if __name__ == '__main__':
    main()
