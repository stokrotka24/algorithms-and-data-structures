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

    k = len(all_data[100]['quick'])
    x = []
    c_dual = []
    c_s_dual = []
    c_quick = []
    c_s_quick = []
    s_dual = []
    s_s_dual = []
    s_quick = []
    s_s_quick = []
    t_dual = []
    t_s_dual = []
    t_quick = []
    t_s_quick = []

    for n in all_data.keys():
        x = np.append(x, [n])

        # comparison = 0
        # moves = 0
        # time = 0
        # for entry in all_data[n]['dual']:
        #     comparison += int(entry['comparisons'])
        #     moves += int(entry['moves'])
        #     time += float(entry['time'][:-1])
        # c_dual = np.append(c_dual, [comparison / k])
        # s_dual = np.append(s_dual, [moves / k])
        # t_dual = np.append(t_dual, [time / k])
        #
        # comparison = 0
        # moves = 0
        # time = 0
        # for entry in all_data[n]['s_dual']:
        #     comparison += int(entry['comparisons'])
        #     moves += int(entry['moves'])
        #     time += float(entry['time'][:-1])
        # c_s_dual = np.append(c_s_dual, [comparison / k])
        # s_s_dual = np.append(s_s_dual, [moves / k])
        # t_s_dual = np.append(t_s_dual, [time / k])

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

        comparison = 0
        moves = 0
        time = 0
        for entry in all_data[n]['s_quick']:
            comparison += int(entry['comparisons'])
            moves += int(entry['moves'])
            time += float(entry['time'][:-1])
        c_s_quick = np.append(c_s_quick, [comparison / k])
        s_s_quick = np.append(s_s_quick, [moves / k])
        t_s_quick = np.append(t_s_quick, [time / k])

    output_file = sys.argv[sys.argv.index('--output') + 1]
    shelf_file = shelve.open(output_file)

    shelf_file['x'] = x
    shelf_file['c_dual'] = c_dual
    shelf_file['c_s_dual'] = c_s_dual
    shelf_file['c_quick'] = c_quick
    shelf_file['c_s_quick'] = c_s_quick
    shelf_file['s_dual'] = s_dual
    shelf_file['s_s_dual'] = s_s_dual
    shelf_file['s_s_quick'] = s_s_quick
    shelf_file['t_quick'] = t_quick
    shelf_file['t_dual'] = t_dual
    shelf_file['t_s_dual'] = t_s_dual
    shelf_file['t_s_quick'] = t_s_quick

    shelf_file.close()

