# This script splits an HC tree into simpler sentences.


import os
import sys
import ipdb
import re
import random
from tqdm import tqdm
from distutils.util import strtobool
import argparse

random.seed(1234)
global args

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inp_fp', type=str)
    parser.add_argument('--out_fp', type=str)
    parser.add_argument('--depth', type=str, default=1)

    return parser

def list_of_conjuncts(string):
    # input - string of conjuncts. eg. "[SS] Ram [ES] and [SS] Shyam [ES]"
    # output - list of conjuncts. eg. ["Ram", "Shyam"]

    # conjuncts = re.findall('\[SS\](.+?)\[ES\]', string)
    conjuncts=[]
    string = string.split()
    depth = 0
    curr_conjunct=[]
    coordinations=["and", "or", ",", "but"]
    for word in string:
        if depth==0 and word.lower() in coordinations:
            continue
        else:
            curr_conjunct.append(word)
        if word=="[SS]":
            depth+=1
        elif word=="[ES]":
            depth-=1
            if depth==0:
                conjuncts.append(" ".join(curr_conjunct[1:-1]))
                curr_conjunct=[]
    
    return conjuncts

# def split_level_1(tree):
#     # splits an HC tree only at depth=1 and returns all resultant sentences in a list
#     sentences=[]
#     # m = re.search('\[SS\](.+?)\[ES\]', tree)
#     # if m:
#     #     found = m.group(1)
#     # m = re.findall('\[D1\](.+?)\[D1\]', tree)
#     if "[D1]" not in tree:
#         sentences = [tree]
#     else:
#         temp = tree.split("[D1]")
#         l = list_of_conjuncts(temp[1].strip())
#         for x in l:
#             sentences.append( temp[0] + x + "[D1]".join(temp[2:]) )
        
#         new_sentences=[]
#         for s in sentences:
#             new_sentences.extend(split_level_1(s))
#         sentences = new_sentences
#         # ipdb.set_trace()
#     return sentences

def split_tree(tree, depth):
    # splits an HC tree only at the specified depth and returns all resultant sentences in a list
    # This function ASSUMES that the input tree is already split at all previous depths
    sentences=[]
    depth_token="[D"+str(depth)+"]"
    # m = re.search('\[SS\](.+?)\[ES\]', tree)
    # if m:
    #     found = m.group(1)
    # m = re.findall('\[D1\](.+?)\[D1\]', tree)
    if depth_token not in tree:
        sentences = [tree]
    else:
        temp = tree.split(depth_token)
        l = list_of_conjuncts(temp[1].strip())
        for x in l:
            sentences.append( temp[0] + x + depth_token.join(temp[2:]) )
        
        new_sentences=[]
        for s in sentences:
            new_sentences.extend(split_tree(s,depth))
        sentences = new_sentences
        # ipdb.set_trace()

    return sentences

def main():
    global args
    parser = parse_args()
    args = parser.parse_args()
    
    trees=open(args.inp_fp,'r').read().strip().split("\n")
    depth=args.depth
    split_sentences=[]
    for tree in trees:
        temp=split_tree(tree,depth)
        temp=[re.sub(" +"," ",t) for t in temp]
        split_sentences.append(temp)
        # break
    
    out_f=open(args.out_fp,'w')
    for tree,sentences in zip(trees, split_sentences):
        out_f.write( tree + "\n---------\n" + "\n".join(sentences) + "\n====================================================\n" )
    out_f.close()

if __name__ == '__main__':
    main()
