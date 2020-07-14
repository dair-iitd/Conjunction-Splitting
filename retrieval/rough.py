import io
import ipdb

def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = [float(x) for x in tokens[1:]] #map(float, tokens[1:])
        ipdb.set_trace()
    return data

data = load_vectors("retrieval/models/minimodel.vec")
ipdb.set_trace()