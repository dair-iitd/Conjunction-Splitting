'''
This script matches sentences with coordinations to their closest sentences without coordinations.
Usage:
python retrieval/matcher1.py --sent_fp data/sentences.txt --conj_fp data/conj_sent.txt --nonconj_fp data/nonconj_sent.txt
'''

import os
import sys
import ipdb
import regex
import random
from tqdm import tqdm
from distutils.util import strtobool
import argparse
import fasttext
import numpy as np

random.seed(1234)
global args

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sent_fp', type=str)
    parser.add_argument('--conj_fp', type=str)
    parser.add_argument('--nonconj_fp', type=str)

    return parser

def encode(model, sent):
    sent = sent.strip().split()
    matrix = np.zeros((len(sent), model.get_dimension()))
    for i in range(len(sent)):
        matrix[i] = model[sent[i]]
    embedding = np.mean(matrix, axis=0)
    return embedding

def main():
    global args
    parser = parse_args()
    args = parser.parse_args()

    # model = fasttext.train_unsupervised(args.sent_fp, model="skipgram")
    # model.save_model("retrieval/models/skipgram.model")
    model = fasttext.load_model("retrieval/models/skipgram.model")
    print("loaded model")

    conj = open(args.conj_fp, 'r').read().strip().split("\n")
    conj = conj[:10]
    nonconj = open(args.nonconj_fp, 'r').read().strip().split("\n")
    nonconj = nonconj[:10000]
    conj_embed, nonconj_embed = [], []
    for sent in conj:
        conj_embed.append(encode(model, sent))
    print("encoded conj sentences")
    for sent in nonconj:
        nonconj_embed.append(encode(model, sent))
    print("encoded nonconj sentences")

    for i in range(len(conj)):
        similarity = np.zeros(len(nonconj))
        for j in range(len(nonconj)):
            similarity[j] = np.dot(conj_embed[i], nonconj_embed[j])
        # ipdb.set_trace()
        idx = np.argsort(similarity)
        print(conj[i])
        print("----------")
        for j in idx[-1:-11:-1]:
            # print(similarity[i], nonconj[j])
            print(nonconj[j])
        print("============================================================")

if __name__ == '__main__':
    main()
