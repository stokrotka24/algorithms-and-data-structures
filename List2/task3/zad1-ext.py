import sys
import math
import time


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


def c_partition(array, low, high, compare):
    p = array[low]
    q = array[high]

    i = low + 1
    k = high - 1
    j = i
    diff = 0

    while j <= k:
        if diff > 0:
            if compare(array[j], p) == -1:
                save_move(array[i])
                save_move(array[j])
                array[i], array[j] = array[j], array[i]
                i = i + 1
                j = j + 1
                diff = diff + 1
            elif compare(array[j], q) == -1:
                j = j + 1
            else:
                save_move(array[j])
                save_move(array[k])
                array[j], array[k] = array[k], array[j]
                k = k - 1
                diff = diff - 1
        else:
            while compare(array[k], q) == 1:
                k = k - 1
                diff = diff - 1
            if j <= k:
                if compare(array[k], p) == -1:
                    save_move(array[k])
                    save_move(array[j])
                    save_move(array[i])
                    array[k], array[j], array[i] = array[j], array[i], array[k]
                    i = i + 1
                    diff = diff + 1
                else:
                    save_move(array[j])
                    save_move(array[k])
                    array[j], array[k] = array[k], array[j]

                j = j + 1

    save_move(array[low])
    save_move(array[i - 1])
    array[low], array[i - 1] = array[i - 1], array[low]

    save_move(array[high])
    save_move(array[k + 1])
    array[high], array[k + 1] = array[k + 1], array[high]

    return i - 1, k + 1


def dual_pivot_quicksort(array, low, high, compare):
    if low < high:
        if compare(array[low], array[high]) == 1:
            save_move(array[low])
            save_move(array[high])
            array[low], array[high] = array[high], array[low]

        pos1, pos2 = c_partition(array, low, high, compare)
        dual_pivot_quicksort(array, low, pos1 - 1, compare)
        dual_pivot_quicksort(array, pos1 + 1, pos2 - 1, compare)
        dual_pivot_quicksort(array, pos2 + 1, high, compare)

    return array


def launch_dual_pivot_quick_sort(array, compare):
    return dual_pivot_quicksort(array, 0, len(array) - 1, compare)


def compare_desc(a, b):
    sys.stderr.write('comparison: ' + str(a) + ' with ' + str(b) + '\n')
    global comp_counter
    comp_counter += 1

    if a < b:
        return 1
    elif a == b:
        return 0
    return -1


def compare_asc(a, b):
    sys.stderr.write('comparison: ' + str(a) + ' with ' + str(b) + '\n')
    global comp_counter
    comp_counter += 1

    if a > b:
        return 1
    elif a == b:
        return 0
    return -1


def save_move(value):
    sys.stderr.write('move: ' + str(value) + '\n')
    global move_counter
    move_counter += 1


def select_algorithm(arg):
    alg_types = {'insert': insertion_sort, 'merge': merge_sort,
                 'quick': launch_quick_sort, 'dual': launch_dual_pivot_quick_sort}
    return alg_types[arg]


def select_compare(arg):
    comp_funcs = {'<=': compare_asc, '>=': compare_desc}
    return comp_funcs[arg]


def check_sorting(array, compare):
    for i in range(0, len(array) - 1):
        if compare(array[i], array[i + 1]) == 1:
            return False

    return True


if __name__ == '__main__':
    comp_counter = 0
    move_counter = 0

    sys.setrecursionlimit(10000)
    try:
        algorithm_name = sys.argv[sys.argv.index('--type') + 1]
        algorithm = select_algorithm(algorithm_name)

        comparator = sys.argv[sys.argv.index('--comp') + 1]
        comp = select_compare(comparator)
    except (ValueError, KeyError):
        print("usage: python3.8 ./task1-ext.py --type insert|merge|quick|dual --comp '>='|'<='")
        sys.exit()

    try:
        n = int(input())
        arr = list(map(int, input().split(' ')[:]))
        if len(arr) != n:
            raise ValueError()
    except ValueError:
        print("enter integral length of list and then proper number of integral values")
        sys.exit()

    comp_counter = 0
    move_counter = 0

    start = time.time()
    arr = algorithm(arr, comp)
    end = time.time()
    delta = (end - start) * 1000

    sys.stderr.write('------- Summary -------\n')
    sys.stderr.write('comparisons: ' + str(comp_counter) + '   ')
    sys.stderr.write('moves: ' + str(move_counter) + '   ')
    sys.stderr.write('time: ' + str(delta) + ' ms \n')

    result_file = open('results.txt', 'a')
    result_file.write('n: ' + str(n) + '  ')
    result_file.write('type: ' + str(algorithm_name) + '  ')
    result_file.write('comparisons: ' + str(comp_counter) + '  ')
    result_file.write('moves: ' + str(move_counter) + '  ')
    result_file.write('time: ' + str(delta) + ' ms \n')
    result_file.close()

    sys.stderr.write('----- Test started -----\n')
    if check_sorting(arr, comp):
        print('n: ' + str(n))
        print(arr)
        sys.stderr.write('----- Test passed ------\n')
    else:
        print('n: ' + str(n) + ' - sorting failed')
        sys.stderr.write('----- Test failed  -----\n')
