import numpy as np
import shelve


def main():
    values = ['small', 'medium', 'big']

    for value in values:
        comp_file = 'results/comp/v_' + value
        with open(comp_file + '.txt') as f:
            results = [int(line.rstrip()) for line in f]

            x = np.array(list(range(1000, 100001, 1000)))
            results = np.array(results)

            shelf_file = shelve.open('parsed_' + comp_file)
            shelf_file['x'] = x
            shelf_file['results'] = results
            shelf_file.close()

        time_file = 'results/time/v_' + value
        with open(time_file + '.txt') as f:
            results = [float(line.rstrip()) for line in f]

            x = np.array(list(range(1000, 100001, 1000)))
            results = np.array(results)

            shelf_file = shelve.open('parsed_' + time_file)
            shelf_file['x'] = x
            shelf_file['results'] = results
            shelf_file.close()

    values = ['nonexistent', 'random']

    for value in values:
        comp_file = 'results/comp/v_' + value
        with open(comp_file + '.txt') as f:
            lines = [int(line.rstrip()) for line in f]

        x = []
        results = []
        for n in range(1000, 100001, 1000):
            x = np.append(x, n)
            a_list = lines[(n // 10) - 100:(n // 10)]
            results = np.append(results, sum(a_list) / len(a_list))

        shelf_file = shelve.open('parsed_' + comp_file)
        shelf_file['x'] = x
        shelf_file['results'] = results
        shelf_file.close()

        time_file = 'results/time/v_' + value
        with open(time_file + '.txt') as f:
            lines = [float(line.rstrip()) for line in f]

        x = []
        results = []
        for n in range(1000, 100001, 1000):
            x = np.append(x, n)
            a_list = lines[(n // 10) - 100:(n // 10)]
            results = np.append(results, sum(a_list) / len(a_list))

        shelf_file = shelve.open('parsed_' + time_file)
        shelf_file['x'] = x
        shelf_file['results'] = results
        shelf_file.close()


if __name__ == '__main__':
    main()
