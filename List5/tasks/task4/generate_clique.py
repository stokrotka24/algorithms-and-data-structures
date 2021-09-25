import random
import sys
from math import sqrt


def generate():
    try:
        n = int(sys.argv[sys.argv.index('-n') + 1])
    except ValueError:
        sys.stderr.write("usage: python3.8 generate_clique.py -n clique_size\n")
        sys.exit()

    a = 5.0

    x = []
    while len(x) != n:
        result = round(random.uniform(0, a), 8)
        if result not in x:
            x.append(result)

    y = []
    while len(y) != n:
        result = round(random.uniform(0, a), 8)
        if result not in y:
            y.append(result)

    file_name = 'g' + str(n) + '.txt'
    results_file = open(file_name, 'w')
    results_file.write(f"{n}\n")

    for u in range(n):
        for v in range(n):
            if u < v:
                w = round(sqrt(pow((x[u] - x[v]), 2) + pow((y[u] - y[v]), 2)), 8)
                results_file.write(f"{u} {v} {w}\n")

    results_file.close()


if __name__ == '__main__':
    generate()
