import random
import time
import re

from BSTConfig import BST, clear_value
from RBTConfig import RBT
from SplayTreeConfig import SplayTree
import sys


def compare(string1, string2):
    global comp_counter
    comp_counter += 1

    if string1 < string2:
        return -1
    if string1 == string2:
        return 0
    return 1


def select_tree(arg):
    tree_types = {'bst': BST, 'rbt': RBT, 'splay': SplayTree}
    return tree_types[arg]


# repeat must be <= 100
def test(repeat_per_n=20, repeat=10):
    tree_types = {'bst': BST, 'rbt': RBT, 'splay': SplayTree}
    with open("words.txt") as f:
        lines = [line.rstrip() for line in f]

    words = lines[:10000]
    additional_words = lines[10000:]
    random.shuffle(words)

    for n in range(100, 10001, 100):
        # select n first words
        n_words = words[:n]

        for i in range(repeat_per_n):
            random.shuffle(n_words)
            additional_entries = random.sample(additional_words, repeat)

            trees_data = {}
            for type_name, tree_type in tree_types.items():
                # create proper type of tree
                tree = tree_type(compare)

                # build tree with n elements
                for word in n_words:
                    tree.insert(word)

                # dictionary to save sum of time for each operation
                operations = {'insert': 0, 'delete': 0, 'find': 0, 'min': 0, 'max': 0, 'successor': 0}
                trees_data[type_name] = [tree, operations]

            entries = list.copy(n_words)
            for j in range(repeat):
                entries.append(additional_entries[j])

                for _, data in trees_data.items():
                    tree = data[0]
                    operations = data[1]

                    start = time.time()
                    tree.insert(additional_entries[j])
                    end = time.time()
                    operations['insert'] += end - start

                value_to_delete = random.choice(entries)
                entries.remove(value_to_delete)

                for _, data in trees_data.items():
                    tree = data[0]
                    operations = data[1]

                    start = time.time()
                    tree.delete(value_to_delete)
                    end = time.time()
                    operations['delete'] += end - start

                value_to_find = random.choice(entries)

                for _, data in trees_data.items():
                    tree = data[0]
                    operations = data[1]

                    start = time.time()
                    tree.find(value_to_find)
                    end = time.time()
                    operations['find'] += end - start

                for _, data in trees_data.items():
                    tree = data[0]
                    operations = data[1]

                    start = time.time()
                    tree.minimum()
                    end = time.time()
                    operations['min'] += end - start

                for _, data in trees_data.items():
                    tree = data[0]
                    operations = data[1]
                    start = time.time()
                    tree.maximum()
                    end = time.time()
                    operations['max'] += end - start

                value_to_find_successor = random.choice(entries)

                for _, data in trees_data.items():
                    tree = data[0]
                    operations = data[1]

                    start = time.time()
                    tree.successor(value_to_find_successor)
                    end = time.time()
                    operations['successor'] += end - start

            for type_name, data in trees_data.items():
                operations = data[1]
                # count average time and save to file
                for op_name, op_time in operations.items():
                    time_file = 'results/' + str(type_name) + '_' + op_name + '.txt'
                    result_file = open(time_file, 'a')
                    result_file.write(str(op_time / repeat) + '\n')
                    result_file.close()


def additional_insert_test():
    tree_types = {'bst': BST, 'rbt': RBT, 'splay': SplayTree}
    with open("aspell_wordlist.txt") as f:
        lines = [line.rstrip() for line in f]

    words = lines[:10000]

    for n in range(100, 10001, 100):
        n_words = words[:n]

        trees_data = {}
        for type_name, tree_type in tree_types.items():
            tree = tree_type(compare)
            for word in n_words:
                tree.insert(word)
            operations = {'insert': 0}
            trees_data[type_name] = [tree, operations]

        for _, data in trees_data.items():
            tree = data[0]
            operations = data[1]

            start = time.time()
            tree.insert(lines[10000])
            end = time.time()
            operations['insert'] += end - start

        for type_name, data in trees_data.items():
            operations = data[1]
            for op_name, op_time in operations.items():
                time_file = 'results_additional/' + str(type_name) + '_' + op_name + '.txt'
                result_file = open(time_file, 'a')
                result_file.write(str(op_time) + '\n')
                result_file.close()


def test2(repeat_per_n=20, repeat=10):
    tree_types = {'bst': BST, 'rbt': RBT, 'splay': SplayTree}

    global comp_counter
    comp_counter = 0

    with open("aspell_wordlist.txt") as f:
        lines = [line.rstrip() for line in f]

    words = lines[:10000]

    for n in range(100, 10001, 100):
        #  select n first words
        n_words = words[:n]

        trees = {}
        for type_name, tree_type in tree_types.items():
            tree = tree_type(compare)
            for word in n_words:
                tree.insert(word)
            trees[type_name] = tree

        # lower, upper bound for bst and splay
        for type_name, tree in trees.items():
            comp_file = 'results_zad2/' + str(type_name) + '_first_elem_asc.txt'
            result_file = open(comp_file, 'a')

            comp_counter = 0
            tree.find(n_words[0])
            result_file.write(str(comp_counter) + '\n')
            result_file.close()

        # new splay tree because tree can be changed by last find operation
        tree = SplayTree(compare)
        for word in n_words:
            tree.insert(word)
        trees['splay'] = tree

        # lower, upper bound for bst and splay
        for type_name, tree in trees.items():
            comp_file = 'results_zad2/' + str(type_name) + '_last_elem_asc.txt'
            result_file = open(comp_file, 'a')

            comp_counter = 0
            tree.find(n_words[-1])
            result_file.write(str(comp_counter) + '\n')
            result_file.close()

        for i in range(repeat_per_n):
            # average for all without duplicates
            find_comp = {'bst': 0, 'rbt': 0, 'splay': 0}

            trees = {}
            random.shuffle(n_words)
            for type_name, tree_type in tree_types.items():
                tree = tree_type(compare)
                for word in n_words:
                    tree.insert(word)
                trees[type_name] = tree

            for j in range(repeat):
                random_word = random.choice(n_words)
                for type_name, tree in trees.items():
                    comp_counter = 0
                    tree.find(random_word)
                    find_comp[type_name] += comp_counter

            for type_name, tree in trees.items():
                comp_file = 'results_zad2/' + str(type_name) + '_random.txt'
                result_file = open(comp_file, 'a')
                result_file.write(str(find_comp[type_name] / repeat) + '\n')
                result_file.close()

    for n in range(100, 10001, 100):
        n_words = words[:n]
        random.shuffle(n_words)
        tree = RBT(compare)
        for word in n_words:
            tree.insert(word)

        comp_counter = 0
        tree.find(tree.root.value)
        comp_file = 'results_zad2/rbt_root.txt'
        result_file = open(comp_file, 'a')
        result_file.write(str(comp_counter) + '\n')
        result_file.close()

    with open("lotr.txt") as file:
        text = file.read()

    raw_words = re.split('[^a-zA-Z0-9_\']+', text)
    words = []
    for raw_word in raw_words:
        try:
            word = clear_value(raw_word)
            words.append(word)
        except IndexError:
            pass

        if len(words) == 10000:
            break

    # average for all with duplicates
    for n in range(100, 10001, 100):
        #  select n first words
        n_words = words[:n]

        for i in range(repeat_per_n):
            find_comp = {'bst': 0, 'rbt': 0, 'splay': 0}

            trees = {}
            random.shuffle(n_words)
            for type_name, tree_type in tree_types.items():
                tree = tree_type(compare)
                for word in n_words:
                    tree.insert(word)
                trees[type_name] = tree

            for j in range(repeat):
                random_word = random.choice(n_words)
                for type_name, tree in trees.items():
                    comp_counter = 0
                    tree.find(random_word)
                    find_comp[type_name] += comp_counter

            for type_name, tree in trees.items():
                comp_file = 'results_zad2/' + str(type_name) + '_random_with_duplicates.txt'
                result_file = open(comp_file, 'a')
                result_file.write(str(find_comp[type_name] / repeat) + '\n')
                result_file.close()


def single_tree():
    try:
        type_name = sys.argv[2]
        tree_type = select_tree(type_name)
        tree = tree_type(compare)
    except (KeyError, IndexError):
        print("usage: python3.8 ./trees.py --type bst|rbt|splay (optional -t for testing purpose)")
        sys.exit()

    try:
        n = int(input())
        lines = []
        for i in range(n):
            lines.append(input())

    except ValueError:
        print("enter integral number of commands and then proper number of commands")
        sys.exit()

    commands_no_args = {'min': tree.minimum, 'max': tree.maximum, 'inorder': tree.inorder}
    commands_with_args = {'insert': tree.insert, 'load': tree.load, 'delete': tree.delete,
                          'find': tree.find, 'successor': tree.successor}

    global comp_counter
    comp_counter = 0
    start = time.time()
    for line in lines:
        split = line.split(" ")
        if len(split) == 1:
            command_name = split[0]
            command = commands_no_args[command_name]
            command()
        if len(split) == 2:
            command_name = split[0]
            arg = split[1]
            command = commands_with_args[command_name]
            command(arg)
    end = time.time()
    delta = end - start
    sys.stderr.write('Type: ' + type_name + '\n')
    sys.stderr.write('Time: ' + str(delta) + ' s \n')
    for operation, occurrences in tree.operations_occ.items():
        sys.stderr.write(operation + ': ' + str(occurrences) + '\n')
    sys.stderr.write('Maximum number of elements in the three: ' + str(tree.max_num_elements) + '\n')
    sys.stderr.write('Number of elements in the three after the session: ' + str(tree.num_elements) + '\n')
    sys.stderr.write('Comparisons between keys in tree: ' + str(comp_counter) + '\n')


def main():
    sys.setrecursionlimit(1000000)

    try:
        arg = sys.argv[1]
        if arg == '-t':
            test()
        elif arg == '-t2':
            test2()
        elif arg == '--type':
            single_tree()
        else:
            raise IndexError
    except IndexError:
        print("usage: python3.8 ./trees.py --type bst|rbt|splay (optional -t for testing purpose)")
        sys.exit()


if __name__ == '__main__':
    comp_counter = 0
    main()
