import shelve

import numpy as np


def main():
    results_files = ['results/random_simple_walk', 'results/greedy_strategy', 'results/strategy_3_kruskal',
                     'results/strategy_3_prim']

    x = []
    k_random = []
    W_random = []
    M_random = []
    T_random = []
    k_greedy = []
    W_greedy = []
    M_greedy = []
    T_greedy = []
    k_kruskal = []
    W_kruskal = []
    M_kruskal = []
    T_kruskal = []
    k_prim = []
    W_prim = []
    M_prim = []
    T_prim = []

    n = 5
    while n <= 2560:
        x = np.append(x, n)
        n *= 2

    with open(results_files[0]) as f:
        lines = [line.rstrip() for line in f]

    for i in range(len(x)):
        part_lines = lines[50 * i:50 * (i + 1)]

        k = []
        W = []
        M = []
        T = []
        for line in part_lines:
            split = line.lstrip().split(" ")
            k.append(int(split[0]))
            W.append(float(split[1]))
            M.append(int(split[2]))
            T.append(float(split[3]))

        k_random = np.append(k_random, sum(k) / len(k))
        W_random = np.append(W_random, sum(W) / len(W))
        M_random = np.append(M_random, sum(M) / len(M))
        T_random = np.append(T_random, sum(T) / len(T))

    output_file = results_files[0] + '_avg'
    result_file = open(output_file, 'w')
    for i in range(len(k_random)):
        result_file.write(f"{k_random[i]} {W_random[i]} {M_random[i]} {T_random[i]}\n")
    result_file.close()

    with open(results_files[1]) as f:
        lines = [line.rstrip() for line in f]

    for line in lines:
        split = line.lstrip().split(" ")
        k_greedy = np.append(k_greedy, int(split[0]))
        W_greedy = np.append(W_greedy, float(split[1]))
        M_greedy = np.append(M_greedy, int(split[2]))
        T_greedy = np.append(T_greedy, float(split[3]))

    with open(results_files[2]) as f:
        lines = [line.rstrip() for line in f]

    for line in lines:
        split = line.lstrip().split(" ")
        k_kruskal = np.append(k_kruskal, int(split[0]))
        W_kruskal = np.append(W_kruskal, float(split[1]))
        M_kruskal = np.append(M_kruskal, int(split[2]))
        T_kruskal = np.append(T_kruskal, float(split[3]))

    with open(results_files[3]) as f:
        lines = [line.rstrip() for line in f]

    for line in lines:
        split = line.lstrip().split(" ")
        k_prim = np.append(k_prim, int(split[0]))
        W_prim = np.append(W_prim, float(split[1]))
        M_prim = np.append(M_prim, int(split[2]))
        T_prim = np.append(T_prim, float(split[3]))

    shelf_file = shelve.open('parsed_results')

    shelf_file['x'] = x
    shelf_file['k_random'] = k_random
    shelf_file['W_random'] = W_random
    shelf_file['M_random'] = M_random
    shelf_file['T_random'] = T_random
    shelf_file['k_greedy'] = k_greedy
    shelf_file['W_greedy'] = W_greedy
    shelf_file['M_greedy'] = M_greedy
    shelf_file['T_greedy'] = T_greedy
    shelf_file['k_kruskal'] = k_kruskal
    shelf_file['W_kruskal'] = W_kruskal
    shelf_file['M_kruskal'] = M_kruskal
    shelf_file['T_kruskal'] = T_kruskal
    shelf_file['k_prim'] = k_prim
    shelf_file['W_prim'] = W_prim
    shelf_file['M_prim'] = M_prim
    shelf_file['T_prim'] = T_prim
    shelf_file.close()


if __name__ == '__main__':
    main()
