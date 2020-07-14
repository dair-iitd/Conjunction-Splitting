# This is an analysis script to identify the fraction of sentences split (on conjunctions) by a system.

import os
import sys
import ipdb
import regex
import random
from tqdm import tqdm
from distutils.util import strtobool
import argparse
import numpy as np

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/samarth/CaRB')

from oie_readers.openieFourReader import OpenieFourReader
from oie_readers.openieFiveReader import OpenieFiveReader

random.seed(1234)
global args

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inp_fp', type=str, required=True)
    parser.add_argument('--out_fp', type=str)
    parser.add_argument('--reader', type=str)

    return parser

def gold_reader(inp_fp):
    lines=open(inp_fp, 'r').read().strip().split('\n')
    d={}
    for l in lines:
        l=l.split('\t')
        if l[0] in d.keys():
            d[l[0]].append('\t'.join(l[1:]))
        else:
            d[l[0]]=['\t'.join(l[1:])]

    return d

def readable_reader(inp_fp):
    sentences=open(inp_fp, 'r').read().strip().split('\n\n')
    d={}
    for lines in sentences:
        lines=lines.split('\n')
        sent=lines[0]
        try:
            exts=[e[e.index('(')+1:-1] for e in lines[1:]]
        except:
            ipdb.set_trace()
        d[sent]=exts
        # if l[0] in d.keys():
        #     d[l[0]].append('\t'.join(l[1:]))
        # else:
        #     d[l[0]]=['\t'.join(l[1:])]

    return d

def main():
    global args
    parser = parse_args()
    args = parser.parse_args()

    if args.reader=="gold":
        d=gold_reader(args.inp_fp)
    elif args.reader=="openiefive":
        predicted = OpenieFiveReader()
        predicted.read(args.inp_fp)
        d=dict()
        for sent,exts in predicted.oie.items():
            temp=[]
            for ext in exts:
                temp.append( ext.args[0]+'\t'+ext.pred+'\t'+'\t'.join(ext.args[1:]) )
            d[sent]=temp
        # ipdb.set_trace()
    elif args.reader=="openiefour":
        predicted = OpenieFourReader()
        predicted.read(args.inp_fp)
        d=dict()
        ipdb.set_trace()
        for sent,exts in predicted.oie.items():
            temp=[]
            for ext in exts:
                temp.append( ext.args[0]+'\t'+ext.pred+'\t'+'\t'.join(ext.args[1:]) )
            d[sent]=temp
    elif args.reader=="readable":
        d=readable_reader(args.inp_fp)
        # ipdb.set_trace()


    sent_with_and=0
    ext_split=0
    for sent,exts in d.items():
        words=sent.split(' ')
        if "and" in words:
            sent_with_and+=1
            try:
                pos=words.index("and")
            except:
                ipdb.set_trace()
            phrase=' '.join(words[pos-1:pos+1])
            ext_split+=1
            for ext in exts:
                if phrase in ext:
                    ext_split-=1
                    break

    print("total_sent={} sent_with_and={} split_sent={} %splits={}".format(len(d.items()), sent_with_and,
                                                                             ext_split, np.round(100*ext_split/sent_with_and,2)))

if __name__ == '__main__':
    main()
