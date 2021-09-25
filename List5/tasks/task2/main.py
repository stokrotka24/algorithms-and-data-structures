import os
import sys
import time
from collections import defaultdict

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from Config import *
from PriorityQueueConfig import *

INF = float('inf')


def make_priority_queue(input_dict):
    queue = PriorityQueue(desc_compare)
    for vertex, distance in input_dict.items():
        queue.insert(vertex, distance)
    return queue


def retrace_path_with_weight(graph, prev, vertex):
    if prev[vertex] is None:
        return str(vertex)
    else:
        return retrace_path_with_weight(graph, prev, prev[vertex]) + " [w = " + str(graph[prev[vertex]][vertex]) \
               + "] " + str(vertex)


def retrace_path(prev, vertex):
    if prev[vertex] is None:
        return str(vertex)
    else:
        return retrace_path(prev, prev[vertex]) + ", " + str(vertex)


def dijkstra(graph, s):
    start = time.time()

    dist = {}
    prev = {}

    for vertex in graph.keys():
        dist[vertex] = INF
        prev[vertex] = None
    dist[s] = 0

    H = make_priority_queue(dist)
    while not H.empty_val():
        u = H.pop_val()

        for z, w in graph[u].items():
            if dist[z] > dist[u] + w:
                dist[z] = dist[u] + w
                prev[z] = u
                H.priority(z, dist[z])

    end = time.time()
    delta = (end - start) * 1000

    print("Id_dest weight_of_path:")
    for vertex, weight in dist.items():
        print(f"{vertex} {weight}")

    sys.stderr.write("Paths with weights: \n")
    for vertex in graph.keys():
        sys.stderr.write(retrace_path_with_weight(graph, prev, vertex) + "\n")

    sys.stderr.write("Paths without weights: \n")
    for vertex in graph.keys():
        sys.stderr.write("[" + retrace_path(prev, vertex) + "]\n")
    sys.stderr.write("Time: " + str(delta) + " ms\n")


def main():
    try:
        n = int(input())
        m = int(input())
        lines = []
        for i in range(m):
            lines.append(input())
        s = int(input())

    except ValueError:
        print("enter n - number vertices, then m - number of directed edges and then enter m edges: u, v, w, "
              "then label of start vertex")
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

    dijkstra(graph, s)


if __name__ == '__main__':
    main()
