#!/usr/bin/env python

import os
import argparse
from pltools.java import get_method_names


def get_args():
    parser = argparse.ArgumentParser(description="Extract all method names from a java source file")
    parser.add_argument("-f", "--java-file", help="Path to java source file")
    args = parser.parse_args()

    return args


def main():
    args = get_args()
    java_file = os.path.abspath(args.java_file)

    for i in get_method_names(java_file):
        print i


if __name__ == '__main__':
    main()
