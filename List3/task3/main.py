import time
import random


def compare(a, b):
    global comp_counter
    comp_counter += 1

    if a > b:
        return 1
    elif a == b:
        return 0
    return -1


def binary_search(array, p, r, v):
    if p > r:
        return 0

    mid = (p + r) // 2
    if compare(v, array[mid]) == 0:
        return 1
    if compare(v, array[mid]) == -1:
        return binary_search(array, p, mid - 1, v)
    return binary_search(array, mid + 1, r, v)


def main():
    global comp_counter

    for n in range(1000, 100001, 1000):
        print(n)
        array = list(range(1, n + 1, 1))
        values = {'small': 100, 'medium': n // 2 - 50, 'big': n - 200}

        for v_name, v_value in values.items():
            comp_counter = 0

            start = time.time()
            result = binary_search(array, 0, len(array) - 1, v_value)
            end = time.time()
            delta = end - start

            comp_file = 'results/comp/v_' + v_name + '.txt'
            result_file = open(comp_file, 'a')
            result_file.write(str(comp_counter) + '\n')
            result_file.close()

            time_file = 'results/time/v_' + v_name + '.txt'
            result_file = open(time_file, 'a')
            result_file.write(str(delta) + '\n')
            result_file.close()

    for n in range(1000, 100001, 1000):
        print(n)
        array = list(range(2, 2 * n + 1, 2))
        values = random.sample(list(range(3, 2 * n, 2)), 100)

        for value in values:
            comp_counter = 0

            start = time.time()
            result = binary_search(array, 0, len(array) - 1, value)
            end = time.time()
            delta = end - start

            comp_file = 'results/comp/v_nonexistent.txt'
            result_file = open(comp_file, 'a')
            result_file.write(str(comp_counter) + '\n')
            result_file.close()

            time_file = 'results/time/v_nonexistent.txt'
            result_file = open(time_file, 'a')
            result_file.write(str(delta) + '\n')
            result_file.close()

    for n in range(1000, 100001, 1000):
        print(n)
        array = list(range(1, n + 1, 1))
        values = random.sample(array, 100)

        for value in values:
            comp_counter = 0

            start = time.time()
            result = binary_search(array, 0, len(array) - 1, value)
            end = time.time()
            delta = end - start

            comp_file = 'results/comp/v_random.txt'
            result_file = open(comp_file, 'a')
            result_file.write(str(comp_counter) + '\n')
            result_file.close()

            time_file = 'results/time/v_random.txt'
            result_file = open(time_file, 'a')
            result_file.write(str(delta) + '\n')
            result_file.close()


if __name__ == '__main__':
    comp_counter = 0
    main()
