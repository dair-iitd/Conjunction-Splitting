# This script separates the distributive and non-distributive sentences into different files to facilitate analysis.

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
    parser.add_argument('--dist_fp', type=str)
    parser.add_argument('--non_dist_fp', type=str)

    return parser

def seperate(inp_fp, dist_fp, non_dist_fp):
    lines = open(inp_fp, 'r').readlines()
    lines = "".join(lines[8:])
    lines = lines.strip().split("====================================================")
    
    dist, non_dist = [],[]
    for l in lines:
        if "DIST" in l:
            dist.append(l)
        if "ND" in l:
            non_dist.append(l)

    dist_f = open(dist_fp, 'w')
    dist_f.write("====================================================".join(dist))
    non_dist_f = open(non_dist_fp, 'w')
    non_dist_f.write("====================================================".join(non_dist))

def main():
    global args
    parser = parse_args()
    args = parser.parse_args()

    seperate(args.inp_fp, args.dist_fp, args.non_dist_fp)

if __name__ == '__main__':
    main()
