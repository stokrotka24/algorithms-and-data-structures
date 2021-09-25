import random

import numpy as np
import statistics as st
import shelve


def main():
    generate_func = ['random_values', 'permutation']
    algorithms = ['randomized_select', 'select']

    for fun in generate_func:
        k_parameters = ['small', 'medium', 'big']
        for k_name in k_parameters:
            for alg in algorithms:
                comp_file = 'results/comp/' + fun + '_' + alg + '_k_' + k_name
                move_file = 'results/move/' + fun + '_' + alg + '_k_' + k_name
                files = [comp_file, move_file]
                for file in files:
                    with open(file + '.txt') as f:
                        lines = [int(line.rstrip()) for line in f]

                    x = []
                    mins = []
                    avgs = []
                    maxs = []
                    stddevs = []
                    points_x = []
                    points_y = []
                    for n in range(100, 10001, 100):
                        x = np.append(x, n)
                        a_list = lines[n - 100:n]
                        mins = np.append(mins, min(a_list))
                        avgs = np.append(avgs, sum(a_list) / len(a_list))
                        maxs = np.append(maxs, max(a_list))
                        stddevs = np.append(stddevs, st.stdev(a_list))
                        sub_list = random.sample(a_list, 20)
                        for elem in sub_list:
                            points_x = np.append(points_x, n)
                            points_y = np.append(points_y, elem)

                    shelf_file = shelve.open('parsed_' + file)
                    shelf_file['x'] = x
                    shelf_file['mins'] = mins
                    shelf_file['avgs'] = avgs
                    shelf_file['maxs'] = maxs
                    shelf_file['stddevs'] = stddevs
                    shelf_file['points_x'] = points_x
                    shelf_file['points_y'] = points_y
                    shelf_file.close()


if __name__ == '__main__':
    main()
