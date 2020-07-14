'''
This script matches sentences with coordinations to their closest sentences without coordinations. This uses pretrained fasttext word embeddings.
Usage:
python retrieval/matcher2.py --conj_fp data/conj_sent.txt --nonconj_fp data/nonconj_sent.txt --mode "weighted" --model retrieval/models/wiki-news-300d-1M.vec --debug
'''

import os
import sys
import ipdb
import regex
import random
from tqdm import tqdm
from distutils.util import strtobool
import argparse
# import fasttext
import numpy as np

import io

random.seed(1234)
global args

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--conj_fp', type=str)
    # parser.add_argument('--sent_mode', type=str, default="unsplit")
    parser.add_argument('--nonconj_fp', type=str)
    parser.add_argument('--model', type=str)
    parser.add_argument('--mode', type=str, default="uniform")
    parser.add_argument('--debug', type=bool, default=False)

    return parser

parser = parse_args()
args = parser.parse_args()
keyerror_count=0

def encode(sent, mode):
    sent = sent.strip().split()
    dim=300 # model.get_dimension()
    matrix = np.zeros((len(sent), dim))
    for i in range(len(sent)):
        try:
            matrix[i] = model[sent[i]]
        except KeyError:
            global keyerror_count
            keyerror_count+=1
            matrix[i] = np.zeros(dim) # unknown words do not affect the sentence embedding since they are encoded to zero vector
    
    if mode=="uniform":
        # Sentence Embedding = Arithmetic Mean of word embeddings
        embedding = np.mean(matrix, axis=0)
    elif mode=="weighted":
        # Sentence Embedding = Weighted Mean of word embeddings, higher weight of words near conjunctions
        embedding = np.zeros(dim)
        window=3
        weight=5
        sum_weights=0
        for i in range(len(sent)):
            if "and" in sent[i-window:i+window+1] or "or" in sent[i-window:i+window+1]:
                embedding+=matrix[i]*weight
                sum_weights+=weight
            else:
                embedding+=matrix[i]
                sum_weights+=1
        embedding/=sum_weights
    else:
        raise Exception("invalid mode")

    return embedding

def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = [float(x) for x in tokens[1:]] #map(float, tokens[1:])
    return data

# model = load_vectors("retrieval/models/wiki-news-300d-1M.vec")
# model = load_vectors("retrieval/models/minimodel.vec")
if args.debug:
    args.model = "retrieval/models/minimodel.vec"
model = load_vectors(args.model)

def main():
    global args
    # model = fasttext.train_unsupervised(args.sent_fp, model="skipgram")
    # model.save_model("retrieval/models/skipgram.model")
    # model = fasttext.load_model("retrieval/models/skipgram.model")
    # print("loaded model")

    print("conj_fp: {} \nnonconj_fp: {}\nmode: {}\nmodel: {}\ndebug:{} \n".format(
            args.conj_fp, args.nonconj_fp, args.mode, args.model, args.debug))

    # if args.sent_mode=="unsplit":
    #     conj = open(args.conj_fp, 'r').read().strip().split("\n")
    # elif args.sent_mode=="split":
    #     temp = open(args.conj_fp, 'r').read().strip().split("\n")
    #     conj = []
    #     for sent in temp:
    #         if sent[:5]!="-----" and sent[:5]!="=====":
    #             conj.append(sent)
    # else:
    #     raise Exception("invalid sent_mode. Valid sent_mode : split , unsplit ")

    temp = open(args.conj_fp, 'r').read().strip().split("\n")
    conj = []
    for sent in temp:
        if sent[:5]!="-----" and sent[:5]!="=====":
            conj.append(sent)

    if args.debug:
        conj = conj[:5]
    else:
        conj = conj[:300]
    nonconj = open(args.nonconj_fp, 'r').read().strip().split("\n")
    if args.debug:
        nonconj = nonconj[:20]
    conj_embed, nonconj_embed = [], []
    for sent in conj:
        conj_embed.append(encode(sent, args.mode))
    print("encoded conj sentences")
    for sent in nonconj:
        nonconj_embed.append(encode(sent, args.mode))
    print("encoded nonconj sentences")
    print("============================================================")

    for i in range(len(conj)):
        similarity = np.zeros(len(nonconj))
        for j in range(len(nonconj)):
            # similarity[j] = np.dot(conj_embed[i], nonconj_embed[j])
            similarity[j] = np.dot(conj_embed[i], nonconj_embed[j]) / (np.linalg.norm(conj_embed[i]) * np.linalg.norm(nonconj_embed[j]) + 1e-8 )

        idx = np.argsort(similarity)
        print(conj[i])
        print("----------")
        for j in idx[-1:-11:-1]:
            print("{:.6f}\t{}".format(similarity[j], nonconj[j]))
            # print(nonconj[j])
        print("============================================================")

    print("keyerror_count: {}".format(keyerror_count))

if __name__ == '__main__':
    main()
