import sys
import math
import time
import random
import shelve

def insertion_sort(array, compare):
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1

        while j >= 0 and compare(array[j], key) == 1:
            save_move(array[j])
            array[j + 1] = array[j]

            j = j - 1
        save_move(key)
        array[j + 1] = key
    return array


def merge(arr1, arr2, compare):
    result = []

    while arr1 and arr2:
        if compare(arr1[0], arr2[0]) == -1:
            save_move(arr1[0])
            result.append(arr1[0])

            arr1 = arr1[1:]
        else:
            save_move(arr2[0])
            result.append(arr2[0])

            arr2 = arr2[1:]

    for elem in arr1 + arr2:
        save_move(elem)

    result = result + arr1 + arr2
    return result


def merge_sort(array, compare):
    length = len(array)

    if length == 1:
        return array
    else:
        midpoint = math.floor(length / 2)
        return merge(merge_sort(array[:midpoint], compare), merge_sort(array[midpoint:], compare), compare)


def partition(array, p, r, compare):
    i = p - 1

    for j in range(p, r):
        if compare(array[j], array[r]) <= 0:
            i = i + 1
            save_move(array[i])
            save_move(array[j])
            array[i], array[j] = array[j], array[i]

    save_move(array[i + 1])
    save_move(array[r])
    array[i + 1], array[r] = array[r], array[i + 1]
    return i + 1


def quick_sort(array, p, r, compare):
    if p < r:
        i = partition(array, p, r, compare)
        quick_sort(array, p, i - 1, compare)
        quick_sort(array, i + 1, r, compare)
    return array


def launch_quick_sort(array, compare):
    return quick_sort(array, 0, len(array) - 1, compare)


def compare_desc(a, b):
    # sys.stderr.write('comparison: ' + str(a) + ' with ' + str(b) + '\n')
    global comp_counter
    comp_counter += 1

    if a < b:
        return 1
    elif a == b:
        return 0
    return -1


def compare_asc(a, b):
    # sys.stderr.write('comparison: ' + str(a) + ' with ' + str(b) + '\n')
    global comp_counter
    comp_counter += 1

    if a > b:
        return 1
    elif a == b:
        return 0
    return -1


def save_move(value):
    # sys.stderr.write('move: ' + str(value) + '\n')
    global move_counter
    move_counter += 1


def select_algorithm(arg):
    alg_types = {'insert': insertion_sort, 'merge': merge_sort, 'quick': launch_quick_sort}
    return alg_types[arg]


def select_compare(arg):
    comp_funcs = {'<=': compare_asc, '>=': compare_desc}
    return comp_funcs[arg]


def select_data_type(arg):
    data_types = {'int': int, 'str': str}
    return data_types[arg]


def check_sorting(array, compare):
    for i in range(0, len(array) - 1):
        if compare(array[i], array[i + 1]) == 1:
            return False

    return True


def sort(algo_name, comp, n, array, file):
    try:
        algorithm = select_algorithm(algo_name)
        compare = select_compare(comp)
    except KeyError:
        print("usage: python3.8 ./search_switch.py --type insert|merge|quick --comp '>='|'<=' --data int|str ("
              "optional: --stat file_name k)")
        sys.exit()

    global comp_counter
    comp_counter = 0

    global move_counter
    move_counter = 0

    start = time.time()
    array = algorithm(array, compare)
    end = time.time()
    delta = (end - start)

    # sys.stderr.write('------- Summary -------\n')
    # sys.stderr.write('comparisons: ' + str(comp_counter) + '   ')
    # sys.stderr.write('moves: ' + str(move_counter) + '   ')
    # sys.stderr.write('time: ' + str(delta) + ' s \n')

    result_file = open(file, 'a')
    result_file.write('n: ' + str(n) + '  ')
    result_file.write('type: ' + str(algo_name) + '  ')
    result_file.write('comparisons: ' + str(comp_counter) + '  ')
    result_file.write('moves: ' + str(move_counter) + '  ')
    result_file.write('time: ' + str(delta) + ' s \n')
    result_file.close()

    # sys.stderr.write('----- Test started -----\n')
    if check_sorting(array, compare):
        print('n: ' + str(n))
        # print(array)
    #     sys.stderr.write('----- Test passed ------\n')
    # else:
    #     sys.stderr.write('----- Test failed  -----\n')


def single_sorting(comp, kind_of_data):
    try:
        algorithm_name = sys.argv[sys.argv.index('--type') + 1]
    except ValueError:
        print(
            "usage: python3.8 ./search_switch.py --type insert|merge|quick --comp '>='|'<=' --data int|str (optional: "
            "--stat file_name k)")
        sys.exit()

    try:
        n = int(input())
        array = list(map(kind_of_data, input().split(' ')[:]))
        if len(array) != n:
            raise ValueError()
    except ValueError:
        print("enter integral length of list and then proper number of integral values")
        sys.exit()

    sort(algorithm_name, comp, n, array, 'results.txt')


def repeating_sorting(comp, file, repeat, kind_of_data):
    algorithms = ['insert', 'merge', 'quick']

    if kind_of_data == int:
        generator = lambda x: list(range(1, x + 1))
    elif kind_of_data == str:
        shelf_file = shelve.open('strings.txt')
        strings = shelf_file['strings']
        shelf_file.close()
        generator = lambda x: strings[:x]

    for n in range(1, 51):
        array = generator(n)

        for i in range(repeat):
            random.shuffle(array)

            for algorithm in algorithms:
                sort(algorithm, comp, n, list.copy(array), file)


if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    comp_counter = 0
    move_counter = 0

    try:
        comparator = sys.argv[sys.argv.index('--comp') + 1]
        data = sys.argv[sys.argv.index('--data') + 1]
        data_type = select_data_type(data)
        if '--stat' in sys.argv:
            file_name = sys.argv[sys.argv.index('--stat') + 1]
            k = int(sys.argv[sys.argv.index('--stat') + 2])
            repeating_sorting(comparator, file_name, k, data_type)
        else:
            single_sorting(comparator, data_type)
    except (ValueError, IndexError):
        print(
            "usage: python3.8 ./search_switch.py --type insert|merge|quick --comp '>='|'<=' --data int|str (optional: "
            "--stat file_name k)")
        sys.exit()
