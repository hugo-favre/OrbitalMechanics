def read_input_file(filename):
    params = {}
    with open('../data/' + filename + '.txt', 'r') as f:
        for line in f:
            line = line.strip()
            key, value = line.split('=')
            key = key.strip()
            params[key] = float(value)
    return params 