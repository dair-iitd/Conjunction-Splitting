'''
This script seperates sentences with and without coordinations.
Usage:
python retrieval/sentence_classifier.py --inp_fp data/sentences.txt --conj_fp data/conj_sent.txt --nonconj_fp data/nonconj_sent.txt
'''

import os
import sys
import ipdb
import regex
import random
from tqdm import tqdm
from distutils.util import strtobool
import argparse

random.seed(1234)
global args

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inp_fp', type=str)
    parser.add_argument('--conj_fp', type=str)
    parser.add_argument('--nonconj_fp', type=str)

    return parser

def contains_conjunct(sent):
    '''
    checks if a sentence has a coordination or not
    NOTE : it does not check whether the coordination is distributive or not
    '''
    sent=sent.strip().split()
    conjunctions=["and", "or"]
    for c in conjunctions:
        if c in sent:
            return True

    return False

def main():
    global args
    parser = parse_args()
    args = parser.parse_args()

    sentences=open(args.inp_fp,'r').read().strip().split("\n")
    conj,nonconj=[],[]
    for s in sentences:
        if contains_conjunct(s):
            conj.append(s)
        else:
	        nonconj.append(s)
    
    print("conj_sent={} nonconj_sent={}".format(len(conj), len(nonconj)))
    open(args.conj_fp,'w').write("\n".join(conj))
    open(args.nonconj_fp,'w').write("\n".join(nonconj))

if __name__ == '__main__':
    main()
