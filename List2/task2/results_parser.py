import sys
import shelve
import numpy as np

if __name__ == '__main__':
    input_file = sys.argv[sys.argv.index('--input') + 1]
    with open(input_file) as f:
        lines = [line.rstrip() for line in f]

    results = []

    for line in lines:
        items = line.split('  ')

        result = {}
        for item in items:
            parts = item.split(': ')
            result[parts[0]] = parts[1]
        results.append(result)

    data = {}
    for result in results:
        num = int(result['n'])
        del result['n']
        data.setdefault(num, [])
        data[num].append(result)

    all_data = {}

    for key, value in data.items():
        all_data.setdefault(key, {})
        dictionary = {}
        for elem in value:
            algo_type = elem['type']
            del elem['type']
            dictionary.setdefault(algo_type, [])
            dictionary[algo_type].append(elem)
        all_data[key] = dictionary

    k = len(all_data[100]['insert'])
    x = []
    c_insert = []
    c_merge = []
    c_quick = []
    s_insert = []
    s_merge = []
    s_quick = []
    t_insert = []
    t_merge = []
    t_quick = []

    for n in all_data.keys():
        x = np.append(x, [n])

        comparison = 0
        moves = 0
        time = 0
        for entry in all_data[n]['insert']:
            comparison += int(entry['comparisons'])
            moves += int(entry['moves'])
            time += float(entry['time'][:-1])
        c_insert = np.append(c_insert, [comparison / k])
        s_insert = np.append(s_insert, [moves / k])
        t_insert = np.append(t_insert, [time / k])

        comparison = 0
        moves = 0
        time = 0
        for entry in all_data[n]['merge']:
            comparison += int(entry['comparisons'])
            moves += int(entry['moves'])
            time += float(entry['time'][:-1])
        c_merge = np.append(c_merge, [comparison / k])
        s_merge = np.append(s_merge, [moves / k])
        t_merge = np.append(t_merge, [time / k])

        comparison = 0
        moves = 0
        time = 0
        for entry in all_data[n]['quick']:
            comparison += int(entry['comparisons'])
            moves += int(entry['moves'])
            time += float(entry['time'][:-1])
        c_quick = np.append(c_quick, [comparison / k])
        s_quick = np.append(s_quick, [moves / k])
        t_quick = np.append(t_quick, [time / k])

    output_file = sys.argv[sys.argv.index('--output') + 1]
    shelf_file = shelve.open(output_file)

    shelf_file['x'] = x
    shelf_file['c_insert'] = c_insert
    shelf_file['c_merge'] = c_merge
    shelf_file['c_quick'] = c_quick
    shelf_file['s_insert'] = s_insert
    shelf_file['s_merge'] = s_merge
    shelf_file['s_quick'] = s_quick
    shelf_file['t_insert'] = t_insert
    shelf_file['t_merge'] = t_merge
    shelf_file['t_quick'] = t_quick

    shelf_file.close()

