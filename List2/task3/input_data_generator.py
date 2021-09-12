import sys
import random


def asc(num):
    for i in range(1, num):
        data.write(str(i) + ' ')
    data.write(str(num))


def desc(num):
    for i in range(num, 1, -1):
        data.write(str(i) + ' ')
    data.write(str(1))


def randomize(num):
    a_list = list(range(1, num + 1))
    random.shuffle(a_list)

    for elem in a_list[:-1]:
        data.write(str(elem) + ' ')
    data.write(str(a_list[-1]))


if __name__ == '__main__':
    n = int(sys.argv[1])
    comparator = sys.argv[2]
    way = sys.argv[3]

    func_map = {'<= sorted': asc, '>= sorted': desc, '<= inversely': desc, '>= inversely': asc, '<= random': randomize,
                '>= random': randomize}
    func = func_map[comparator + ' ' + way]
    data = open('input_data.txt', 'w')
    data.write(str(n) + '\n')
    func(n)
    data.write('\n')
    data.close()
