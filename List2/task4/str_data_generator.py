import sys
import random
import shelve


def asc(num, words):
    for word in words[:num - 1]:
        data.write(word + ' ')
    data.write(words[num - 1])


def desc(num, words):
    words = words[:num]
    words.reverse()

    for word in words[:num - 1]:
        data.write(word + ' ')
    data.write(words[num - 1])


def randomize(num, words):
    words = words[:num]
    random.shuffle(words)

    for word in words[:num - 1]:
        data.write(word + ' ')
    data.write(words[num - 1])


if __name__ == '__main__':
    n = int(sys.argv[1])
    comparator = sys.argv[2]
    way = sys.argv[3]

    func_map = {'<= sorted': asc, '>= sorted': desc, '<= inversely': desc, '>= inversely': asc, '<= random': randomize,
                '>= random': randomize}

    shelf_file = shelve.open('strings.txt')
    strings = shelf_file['strings']
    shelf_file.close()

    func = func_map[comparator + ' ' + way]
    data = open('input_data.txt', 'w')
    data.write(str(n) + '\n')
    func(n, strings)
    data.write('\n')
    data.close()
