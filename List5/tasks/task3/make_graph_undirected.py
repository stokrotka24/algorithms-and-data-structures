import sys


def main():
    try:
        input_file = sys.argv[sys.argv.index('--input') + 1]
    except ValueError:
        sys.stderr.write("usage: python3.8 make_graph_undirected.py --input file_name (WITHOUT extension)\n")
        sys.exit()
    with open('../task2/' + input_file + '.txt') as f:
        lines = [line.rstrip() for line in f]

    n = int(lines[0])
    lines = lines[2:]

    pairs = set()
    output_lines = []
    for line in lines:
        split = line.lstrip().split(" ")
        if len(split) == 3:
            u = int(split[0])
            v = int(split[1])
            if v > u:
                u, v = v, u

            w = float(split[2])

            cond1 = 0 <= u <= n - 1
            cond2 = 0 <= v <= n - 1
            cond3 = w >= 0
            cond4 = (u, v) not in pairs

            if cond1 and cond2 and cond3 and cond4:
                pairs.add((u, v))
                output_lines.append(line)

    m = len(output_lines)

    output_file = input_file + '_un.txt'

    graph_file = open(output_file, 'w')
    graph_file.write(str(n) + '\n')
    graph_file.write(str(m) + '\n')
    for output_line in output_lines:
        graph_file.write(output_line + '\n')
    graph_file.close()


if __name__ == '__main__':
    main()
