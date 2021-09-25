import numpy as np
import shelve


def main():
    tree_types = ['bst', 'rbt', 'splay']
    operations = ['insert', 'delete', 'find', 'min', 'max', 'successor']
    repeat = 20

    for tree_type in tree_types:
        for operation in operations:
            time_file = 'results/' + tree_type + '_' + operation
            with open(time_file + '.txt') as f:
                lines = [float(line.rstrip()) for line in f]

            x = []
            # mins = []
            avgs = []
            # maxs = []
            # stddevs = []
            # points_x = []
            # points_y = []
            i = 0
            for n in range(100, 10001, 100):
                x = np.append(x, n)
                a_list = lines[i * repeat: (i + 1) * repeat]
                # mins = np.append(mins, min(a_list))
                avgs = np.append(avgs, sum(a_list) / len(a_list))
                # maxs = np.append(maxs, max(a_list))
                # stddevs = np.append(stddevs, st.stdev(a_list))
                # sub_list = random.sample(a_list, 20)
                # for elem in sub_list:
                #     points_x = np.append(points_x, n)
                #     points_y = np.append(points_y, elem)
                i = i + 1

            shelf_file = shelve.open('parsed_' + time_file)
            shelf_file['x'] = x
            # shelf_file['mins'] = mins
            shelf_file['avgs'] = avgs
            # shelf_file['maxs'] = maxs
            # shelf_file['stddevs'] = stddevs
            # shelf_file['points_x'] = points_x
            # shelf_file['points_y'] = points_y
            shelf_file.close()


if __name__ == '__main__':
    main()
