from random import randint


def generate(n=1000):
    result_file = open('input.txt', 'w')

    result_file.write('empty\n')
    result_file.write('print\n')

    for i in range(n):
        x = randint(-n // 4, n // 4)
        p = randint(0, n - 1)
        result_file.write(f"insert {x} {p}\n")

    result_file.write('empty\n')
    result_file.write('print\n')
    result_file.write('top\n')
    result_file.write('pop\n')
    result_file.write('empty\n')
    result_file.write('print\n')
    result_file.write('priority 0 0\n')
    result_file.write('print\n')

    for i in range(n):
        result_file.write('pop\n')

    result_file.write('empty\n')
    result_file.write('top\n')
    result_file.write('priority 0 0\n')
    result_file.write('print\n')
    result_file.close()


if __name__ == '__main__':
    generate()
