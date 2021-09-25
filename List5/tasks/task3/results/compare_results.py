import sys


def main():
    try:
        input_file = sys.argv[sys.argv.index('--input') + 1]
    except ValueError:
        sys.stderr.write("--input file_name (WITHOUT extension)\n")
        sys.exit()

    list_of_lines = []
    files = []
    ways = ['impl', 'lib']
    algorithms = ['kruskal', 'prim']
    for way in ways:
        for algorithm in algorithms:
            file = input_file + '_' + way + '_' + algorithm + '.txt'
            files.append(file)
            with open(file) as f:
                lines = [line.rstrip() for line in f]
            list_of_lines.append(lines)

    results_matched = True
    length = len(list_of_lines)
    for i in range(length):
        index1 = i
        index2 = (i + 1) % length
        first_lines = list_of_lines[index1]
        second_lines = list_of_lines[index2]

        for first_line in first_lines:
            if first_line not in second_lines:
                print(f"In {files[index1]} we have line: {first_line}, which we doesn't have in {files[index2]}")
                results_matched = False

        for second_line in second_lines:
            if second_line not in first_lines:
                print(f"In {files[index2]} we have line: {second_line}, which we doesn't have in {files[index1]}")
                results_matched = False
    print(results_matched)


if __name__ == '__main__':
    main()
