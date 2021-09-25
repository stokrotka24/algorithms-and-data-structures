import sys
import networkx as nx
from matplotlib import pyplot as plt


def main():
    try:
        impl_file = sys.argv[sys.argv.index('--impl_file') + 1]
        lib_file = sys.argv[sys.argv.index('--lib_file') + 1]
        n = int(sys.argv[sys.argv.index('-n') + 1])
    except ValueError:
        sys.stderr.write("usage: python3.8 compare_results.py --impl_file file_name1 --lib_file file_name2\n")
        sys.exit()

    with open(impl_file) as f:
        impl_lines = [line.rstrip() for line in f]

    with open(lib_file) as f:
        lib_lines = [line.rstrip() for line in f]

    impl_lines = impl_lines[n * 2 + 3:-1]
    paths_matched = True
    for lib_line in lib_lines:
        if lib_line not in impl_lines:
            print(f"In {lib_file} we have line: {lib_line}, which we doesn't have in {impl_file}")
            paths_matched = False

    for impl_line in impl_lines:
        if impl_line not in lib_lines:
            print(f"In {impl_file} we have line: {impl_line}, which we doesn't have in {lib_file}")
            paths_matched = False

    print(paths_matched)


if __name__ == '__main__':
    main()
