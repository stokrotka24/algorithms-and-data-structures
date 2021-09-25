import os
import random
import sys
import time
from collections import defaultdict
from random import randint

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from Config import *
from PriorityQueueConfig import *

INF = float('inf')
parent = {}
rank = {}
k = 0
W = 0
M = 0
T = 0
prev_vertex = 0


def all_visited(visited):
    for value in visited:
        if not value:
            return False
    return True


def random_simple_walk(graph, n):
    global k
    global W
    global M
    global T
    k = 0
    W = 0
    M = 0
    T = 0

    start = time.time()
    start_vertex = randint(0, n - 1)

    trace = []
    visited = []
    for i in range(n):
        visited.append(False)

    curr_vertex = start_vertex
    visited[curr_vertex] = 1

    while not all_visited(visited):
        next_vertex = random.choice(list(graph[curr_vertex].keys()))
        weight = graph[curr_vertex][next_vertex]
        k += 1
        W += weight

        trace.append(({curr_vertex, next_vertex}, weight))
        curr_vertex = next_vertex
        visited[curr_vertex] = True

    end = time.time()
    M += sys.getsizeof(trace) + sys.getsizeof(visited) + 3 * sys.getsizeof(curr_vertex) + sys.getsizeof(float('inf'))
    # 2 * sys.getsizeof(curr_vertex) - size of curr_vertex, next_vertex and start_vertex
    # sys.getsizeof(float('inf')) - size of weight
    T = end - start
    return trace


def greedy_strategy(graph, n):
    global k
    global W
    global M
    global T
    k = 0
    W = 0
    M = 0
    T = 0

    start = time.time()
    start_vertex = randint(0, n - 1)

    unvisited = []
    trace = []

    for i in range(n):
        unvisited.append(i)

    M += sys.getsizeof(unvisited)
    curr_vertex = start_vertex
    unvisited.remove(curr_vertex)

    while unvisited:
        min_weight = float('inf')
        for vertex in unvisited:
            if graph[curr_vertex][vertex] < min_weight:
                next_vertex = vertex
                min_weight = graph[curr_vertex][vertex]

        weight = graph[curr_vertex][next_vertex]
        k += 1
        W += weight

        trace.append(({curr_vertex, next_vertex}, weight))
        curr_vertex = next_vertex
        unvisited.remove(curr_vertex)

    end = time.time()
    M += sys.getsizeof(trace) + 3 * sys.getsizeof(curr_vertex) + 2 * sys.getsizeof(float('inf'))
    # 2 * sys.getsizeof(curr_vertex) - size of curr_vertex, next_vertex and start_vertex
    # 2 * sys.getsizeof(float('inf')) - size of weight and min_weight
    T = end - start
    return trace


def make_set(x):
    parent[x] = x
    rank[x] = 0


def make_priority_queue_from_graph(input_graph):
    queue = PriorityQueue(desc_compare)
    for u in input_graph.keys():
        for v, w in input_graph[u].items():
            if u < v:
                queue.insert({u, v}, w)
    return queue


def make_priority_queue(input_dict):
    queue = PriorityQueue(desc_compare)
    for vertex, distance in input_dict.items():
        queue.insert(vertex, distance)
    return queue


def find(x):
    if x != parent[x]:
        parent[x] = find(parent[x])
    return parent[x]


def union(x, y):
    r_x = find(x)
    r_y = find(y)
    if r_x == r_y:
        return
    if rank[r_x] > rank[r_y]:
        parent[r_y] = r_x
    else:
        parent[r_x] = r_y

    if rank[r_x] == rank[r_y]:
        rank[r_y] += 1


def kruskal(graph, n):
    global M

    for vertex in range(n):
        make_set(vertex)

    X = defaultdict(dict)
    sum_weights = 0

    Q = make_priority_queue_from_graph(graph)
    M += sys.getsizeof(Q)
    while not Q.empty_val():
        edge = Q.pop_val()
        u, v = edge
        if find(u) != find(v):
            weight = graph[u][v]
            X[u][v] = weight
            X[v][u] = weight
            sum_weights += weight
            union(u, v)

    M += sys.getsizeof(parent) + sys.getsizeof(rank) + sys.getsizeof(X) + sys.getsizeof(sum_weights) + sys.getsizeof(
        edge) + 5 * sys.getsizeof(u)
    # 5 * sys.getsizeof(u) - size of u, v, weight and r_x and r_y from union

    return X, sum_weights


def prim(graph, n, s):
    global M

    cost = {}
    prev = {}

    for vertex in range(n):
        cost[vertex] = INF
        prev[vertex] = None
    cost[s] = 0

    H = make_priority_queue(cost)
    M += sys.getsizeof(H)
    while not H.empty_val():
        v = H.pop_val()

        for z, w in graph[v].items():
            if H.contains(z) and cost[z] > w:
                cost[z] = w
                prev[z] = v
                H.priority(z, cost[z])

    X = defaultdict(dict)
    sum_weights = 0
    for vertex, c in cost.items():
        if prev[vertex] is not None:
            if prev[vertex] < vertex:
                u, v = prev[vertex], vertex
            else:
                u, v = vertex, prev[vertex]

            X[u][v] = c
            X[v][u] = c
            sum_weights += c

    M += sys.getsizeof(cost) + sys.getsizeof(prev) + 2 * sys.getsizeof(v) + sys.getsizeof(X) + sys.getsizeof(
        sum_weights)
    # 2 * sys.getsizeof(v) - size of v, u
    return X, sum_weights


def explore(visited, trace, graph, MST, v):
    global k
    global W
    global M
    global prev_vertex
    visited[v] = True

    for z in MST[v].keys():
        if not visited[z]:
            weight = graph[prev_vertex][z]
            k += 1
            W += weight
            trace.append(({prev_vertex, z}, weight))
            prev_vertex = z
            explore(visited, trace, graph, MST, z)


def strategy_3(graph, n, algorithm):
    global k
    global W
    global M
    global T
    global prev_vertex
    k = 0
    W = 0
    M = 0
    T = 0
    prev_vertex = 0

    start = time.time()

    start_vertex = randint(0, n - 1)
    if algorithm == "k":
        MST, _ = kruskal(graph, n)
    else:
        MST, _ = prim(graph, n, start_vertex)

    visited = []
    trace = []

    for i in range(n):
        visited.append(False)

    prev_vertex = start_vertex
    explore(visited, trace, graph, MST, start_vertex)

    M += sys.getsizeof(MST) + sys.getsizeof(visited) + sys.getsizeof(trace) + sys.getsizeof(start_vertex) \
         + sys.getsizeof(prev_vertex) + sys.getsizeof(float('inf'))
    # sys.getsizeof(float('inf')) - for weight in explore()
    end = time.time()
    T = end - start
    return trace


def test():
    global k
    global W
    global M
    global T
    k = 0
    W = 0
    M = 0
    T = 0
    results_files = ['results/random_simple_walk', 'results/greedy_strategy', 'results/strategy_3_kruskal',
                     'results/strategy_3_prim']

    n = 5
    while n <= 2560:
        print(n)
        with open('g' + str(n) + '.txt') as f:
            lines = [line.rstrip() for line in f]
        lines = lines[1:]

        graph = defaultdict(dict)
        for line in lines:
            split = line.lstrip().split(" ")
            if len(split) == 3:
                u = int(split[0])
                v = int(split[1])
                w = float(split[2])

                cond1 = 0 <= u <= n - 1
                cond2 = 0 <= v <= n - 1
                cond3 = w >= 0

                if cond1 and cond2 and cond3:
                    graph[u][v] = w
                    graph[v][u] = w

        for j in range(50):
            trace = random_simple_walk(graph, n)
            result_file = open(results_files[0], 'a')
            result_file.write(f"{k} {W} {M} {T}\n")
            result_file.close()

        result_file = open(results_files[0] + '_trace', 'a')
        result_file.write(f"{trace}\n")
        result_file.close()

        trace = greedy_strategy(graph, n)
        result_file = open(results_files[1], 'a')
        result_file.write(f"{k} {W} {M} {T}\n")
        result_file.close()

        result_file = open(results_files[1] + '_trace', 'a')
        result_file.write(f"{trace}\n")
        result_file.close()

        trace = strategy_3(graph, n, algorithm="k")
        result_file = open(results_files[2], 'a')
        result_file.write(f"{k} {W} {M} {T}\n")
        result_file.close()

        result_file = open(results_files[2] + '_trace', 'a')
        result_file.write(f"{trace}\n")
        result_file.close()

        trace = strategy_3(graph, n, algorithm="p")
        result_file = open(results_files[3], 'a')
        result_file.write(f"{k} {W} {M} {T}\n")
        result_file.close()

        result_file = open(results_files[3] + '_trace', 'a')
        result_file.write(f"{trace}\n")
        result_file.close()
        n *= 2


def main():
    try:
        arg = sys.argv[1]
        if arg == "-t":
            test()
            sys.exit()
    except IndexError:
        pass

    try:
        n = int(input())
        m = (n * (n - 1)) // 2
        lines = []
        for i in range(m):
            lines.append(input())
    except ValueError:
        print("enter n - number vertices, enter m undirected edges (remember about triangle inequality): u, v, w"
              "vertex")
        sys.exit()

    graph = defaultdict(dict)

    for line in lines:
        split = line.lstrip().split(" ")
        if len(split) == 3:
            u = int(split[0])
            v = int(split[1])
            w = float(split[2])

            cond1 = 0 <= u <= n - 1
            cond2 = 0 <= v <= n - 1
            cond3 = w >= 0

            if cond1 and cond2 and cond3:
                graph[u][v] = w
                graph[v][u] = w

    global k
    global W
    global M
    global T
    k = 0
    W = 0
    M = 0
    T = 0

    trace = random_simple_walk(graph, n)
    print(f"{k} {W} {M} {T}")
    sys.stderr.write(f"{trace}\n")

    trace = greedy_strategy(graph, n)
    print(f"{k} {W} {M} {T}")
    sys.stderr.write(f"{trace}\n")

    trace = strategy_3(graph, n, algorithm="k")
    print(f"{k} {W} {M} {T}")
    sys.stderr.write(f"{trace}\n")

    trace = strategy_3(graph, n, algorithm="p")
    print(f"{k} {W} {M} {T}")
    sys.stderr.write(f"{trace}\n")


if __name__ == '__main__':
    main()
