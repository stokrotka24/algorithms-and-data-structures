import numpy as np
import shelve


def main():
    generate_func = ['permutation']
    group_sizes = [i for i in range(3, 26, 2)]

    for fun in generate_func:
        k_parameters = ['small', 'medium', 'big']
        for k_name in k_parameters:
            for size in group_sizes:
                comp_file = 'results_zad2/comp/' + str(fun) + '_group_' + str(size) + '_k_' + k_name
                move_file = 'results_zad2/move/' + str(fun) + '_group_' + str(size) + '_k_' + k_name

                files = [comp_file, move_file]
                for file in files:
                    with open(file + '.txt') as f:
                        lines = [int(line.rstrip()) for line in f]

                    x = []
                    avgs = []
                    for n in range(100, 10001, 100):
                        x = np.append(x, n)
                        a_list = lines[n - 100:n]
                        avgs = np.append(avgs, sum(a_list) / len(a_list))

                    shelf_file = shelve.open('parsed_' + file)
                    shelf_file['x'] = x
                    shelf_file['avgs'] = avgs
                    shelf_file.close()

                time_file = 'results_zad2/time/' + str(fun) + '_group_' + str(size) + '_k_' + k_name
                with open(time_file + '.txt') as f:
                    lines = [float(line.rstrip()) for line in f]

                x = []
                avgs = []

                for n in range(100, 10001, 100):
                    x = np.append(x, n)
                    a_list = lines[n - 100:n]
                    avgs = np.append(avgs, sum(a_list) / len(a_list))

                shelf_file = shelve.open('parsed_' + time_file)
                shelf_file['x'] = x
                shelf_file['avgs'] = avgs
                shelf_file.close()


if __name__ == '__main__':
    main()
