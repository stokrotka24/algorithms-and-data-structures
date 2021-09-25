import os
import sys
from collections import defaultdict

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from Config import *
from PriorityQueueConfig import *

INF = float('inf')
parent = {}
rank = {}


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
    for vertex in range(n):
        make_set(vertex)

    X = []
    sum_weights = 0

    Q = make_priority_queue_from_graph(graph)
    while not Q.empty_val():
        edge = Q.pop_val()
        u, v = edge
        if find(u) != find(v):
            weight = graph[u][v]
            X.append((edge, weight))
            sum_weights += weight
            union(u, v)
    return X, sum_weights


def prim(graph, n, s):
    cost = {}
    prev = {}

    for vertex in range(n):
        cost[vertex] = INF
        prev[vertex] = None
    cost[s] = 0

    H = make_priority_queue(cost)
    while not H.empty_val():
        v = H.pop_val()

        for z, w in graph[v].items():
            if H.contains(z) and cost[z] > w:
                cost[z] = w
                prev[z] = v
                H.priority(z, cost[z])

    X = []
    sum_weights = 0
    for vertex, c in cost.items():
        if prev[vertex] is not None:
            if prev[vertex] < vertex:
                u, v = prev[vertex], vertex
            else:
                u, v = vertex, prev[vertex]

            X.append(({u, v}, c))
            sum_weights += c
    return X, sum_weights


def main():
    try:
        algorithm_name = sys.argv[1]
        if algorithm_name != '-p' and algorithm_name != '-k':
            raise IndexError
    except IndexError:
        sys.stderr.write("usage: python3.8 main.py -p|-k\n")
        sys.exit()

    try:
        n = int(input())
        m = int(input())
        lines = []
        for i in range(m):
            lines.append(input())

    except ValueError:
        print("enter n - number vertices, then m - number of undirected edges and then enter m edges: u, v, w"
              "vertex")
        sys.exit()

    graph = defaultdict(dict)
    for i in range(n):
        graph[i][i] = 0

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

    X = []
    sum_weights = 0
    if algorithm_name == '-p':
        X, sum_weights = prim(graph, n, 0)
    elif algorithm_name == '-k':
        X, sum_weights = kruskal(graph, n)

    for edge in X:
        u, v = edge[0]
        if u > v:
            u, v = v, u
        w = edge[1]
        print(f"{u} {v} {w}")
    print(sum_weights)


if __name__ == '__main__':
    main()
