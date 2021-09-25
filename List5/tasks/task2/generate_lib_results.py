import sys
import networkx as nx
from matplotlib import pyplot as plt


def main():
    try:
        input_file = sys.argv[sys.argv.index('--input') + 1]
    except ValueError:
        sys.stderr.write("usage: python3.8 generate_lib_results.py --input file_name (WITHOUT extension)\n")
        sys.exit()

    with open(input_file + '.txt') as f:
        lines = [line.rstrip() for line in f]

    n = int(lines[0])
    start_node = int(lines[-1])
    lines = lines[2:-1]
    graph = nx.DiGraph()

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
                graph.add_edge(u, v, w=w)

    # plt.figure(figsize=(20, 20))
    # pos = nx.spring_layout(graph)
    # nx.draw_networkx_edge_labels(graph, pos)
    # nx.draw_networkx_labels(graph, pos, font_color="w")
    # nx.draw(graph, pos)
    # plt.savefig("graph.png")

    output_file = 'results/' + input_file + '_lib.txt'
    results_file = open(output_file, 'w')

    for node in graph.nodes:
        path = nx.shortest_path(graph, start_node, node, weight='w', method='dijkstra')
        results_file.write(str(path) + '\n')

    results_file.close()

if __name__ == '__main__':
    main()
