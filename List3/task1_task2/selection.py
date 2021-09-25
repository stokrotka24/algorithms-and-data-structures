import random
import sys
import time


def compare(a, b):
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


def partition(array, p, r):
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


def randomized_partition(array, p, r):
    i = random.randint(p, r)
    sys.stderr.write('chosen pivot: ' + str(array[i]) + '\n')

    save_move(array[i])
    save_move(array[r])
    array[i], array[r] = array[r], array[i]
    return partition(array, p, r)


def randomized_select(array, p, r, i):
    if p == r:
        return array[p]
    q = randomized_partition(array, p, r)  # index of pivot in array
    k = q - p + 1  # order statistic of pivot in array[p..r]
    if i == k:
        return array[q]
    if i < k:
        return randomized_select(array, p, q - 1, i)
    return randomized_select(array, q + 1, r, i - k)


def insertion_sort(array, p, r):
    for i in range(p + 1, r + 1):
        key = array[i]
        j = i - 1

        while j >= p and compare(array[j], key) == 1:
            save_move(array[j])
            array[j + 1] = array[j]

            j = j - 1
        save_move(key)
        array[j + 1] = key


def select(array, p, r, i, group_length=5):
    length = r - p + 1

    if length == 1:
        return array[p]

    medians = []
    result, rest = divmod(length, group_length)

    for j in range(result):
        low = p + j * group_length
        mid = low + group_length // 2
        insertion_sort(array, low, low + group_length - 1)
        medians.append(array[mid])

    if rest != 0:
        low = p + result * group_length
        mid = low + ((r - low) // 2)
        insertion_sort(array, low, r)
        medians.append(array[mid])

    median_of_medians = select(medians, 0, len(medians) - 1, (len(medians) - 1) // 2 + 1)
    sys.stderr.write('chosen pivot: ' + str(median_of_medians) + '\n')

    for j in range(p, r + 1):  # find index of median_of_medians
        if compare(array[j], median_of_medians) == 0:
            save_move(array[j])
            save_move(array[r])
            array[j], array[r] = array[r], array[j]
            break

    q = partition(array, p, r)  # index of pivot in array
    k = q - p + 1  # order statistic of pivot in array[p..r]
    if i == k:
        return median_of_medians
    if i < k:
        return select(array, p, q - 1, i)
    return select(array, q + 1, r, i - k)


def random_values(n):
    return random.sample(range(50000), n)


def permutation(n):
    a_list = list(range(1, n + 1))
    random.shuffle(a_list)
    return a_list


def launch_algos(array, k):
    sys.stderr.write('array: ' + str(array) + '\n')
    sys.stderr.write('k = ' + str(k) + '\n')
    algorithms = [randomized_select, select]
    global comp_counter
    global move_counter

    for alg in algorithms:
        sys.stderr.write('algorithm: ' + str(alg.__name__) + '\n')
        arr_copy = list.copy(array)
        comp_counter = 0
        move_counter = 0

        stat = alg(arr_copy, 0, len(arr_copy) - 1, k)
        for elem in arr_copy:
            if elem == stat:
                print('[' + str(elem) + ']', end=' ')
            else:
                print(elem, end=' ')
        print()
        sys.stderr.write('------- Summary -------\n')
        sys.stderr.write('comparisons: ' + str(comp_counter) + '\n')
        sys.stderr.write('moves: ' + str(move_counter) + '\n')
        sys.stderr.write('-----------------------\n')


def single_selection(generate):
    try:
        n = int(input())
        k = int(input())
        if k < 1 or k > n:
            raise ValueError()
    except ValueError:
        print('enter n - integral length of list and then k - proper order statistic (1 <= k <= n)')
        sys.exit()

    array = generate(n)
    launch_algos(array, k)


def testing_selection():
    generate_func = [random_values, permutation]
    algorithms = [randomized_select, select]
    repeat = 100

    global comp_counter
    global move_counter

    for fun in generate_func:
        for n in range(100, 10001, 100):
            print(n)
            k_parameters = {'small': 10, 'medium': n / 2, 'big': n - 5}
            for k_name, k_value in k_parameters.items():
                for _ in range(repeat):
                    array = fun(n)

                    for alg in algorithms:
                        arr_copy = list.copy(array)
                        comp_counter = 0
                        move_counter = 0

                        stat = alg(arr_copy, 0, len(arr_copy) - 1, k_value)
                        comp_file = 'results/comp/' + str(fun.__name__) + '_' + str(
                            alg.__name__) + '_k_' + k_name + '.txt'
                        result_file = open(comp_file, 'a')
                        result_file.write(str(comp_counter) + '\n')
                        result_file.close()

                        move_file = 'results/move/' + str(fun.__name__) + '_' + str(
                            alg.__name__) + '_k_' + k_name + '.txt'
                        result_file = open(move_file, 'a')
                        result_file.write(str(move_counter) + '\n')
                        result_file.close()


def test_group_size():
    generate_func = [permutation]
    group_sizes = [i for i in range(3, 26, 2)]
    repeat = 100

    global comp_counter
    global move_counter

    for fun in generate_func:
        for n in range(100, 10001, 100):
            print(n)
            k_parameters = {'small': 10, 'medium': n / 2, 'big': n - 5}
            for k_name, k_value in k_parameters.items():
                for _ in range(repeat):
                    array = fun(n)

                    for size in group_sizes:
                        arr_copy = list.copy(array)
                        comp_counter = 0
                        move_counter = 0

                        start = time.time()
                        stat = select(arr_copy, 0, len(arr_copy) - 1, k_value, size)
                        end = time.time()
                        delta = (end - start) * 1000

                        comp_file = 'results_zad2/comp/' + str(fun.__name__) + '_group_' + str(
                            size) + '_k_' + k_name + '.txt'
                        result_file = open(comp_file, 'a')
                        result_file.write(str(comp_counter) + '\n')
                        result_file.close()

                        move_file = 'results_zad2/move/' + str(fun.__name__) + '_group_' + str(
                            size) + '_k_' + k_name + '.txt'
                        result_file = open(move_file, 'a')
                        result_file.write(str(move_counter) + '\n')
                        result_file.close()

                        time_file = 'results_zad2/time/' + str(fun.__name__) + '_group_' + str(
                            size) + '_k_' + k_name + '.txt'
                        result_file = open(time_file, 'a')
                        result_file.write(str(delta) + '\n')
                        result_file.close()


def main():
    sys.setrecursionlimit(10000)

    try:
        arg = sys.argv[1]
        if arg == '-r':
            generate_func = random_values
            single_selection(generate_func)
        elif arg == '-p':
            generate_func = permutation
            single_selection(generate_func)
        elif arg == '-t1':
            testing_selection()
            sys.exit()
        elif arg == '-t2':
            test_group_size()
            sys.exit()
        else:
            raise IndexError
    except IndexError:
        print('usage: python3.8 ./selection.py -r|-p (optional -t for testing purpose)')
        sys.exit()


if __name__ == '__main__':
    comp_counter = 0
    move_counter = 0
    main()
