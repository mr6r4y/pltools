#!/usr/bin/env python

import os
import argparse
from pltools.ansic import CAnalysis


def get_args():
    parser = argparse.ArgumentParser(description="Extract all function names from c source file")
    parser.add_argument("-c", "--c-file", help="Path to c source file")
    args = parser.parse_args()

    return args


def main():
    args = get_args()
    c_file = os.path.abspath(args.c_file)

    a = CAnalysis(c_file).get_defined_functions()

    for i in a:
        print i


if __name__ == '__main__':
    main()
