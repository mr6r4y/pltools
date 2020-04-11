import os
import sys
import argparse
from .java import format_class_dot_node, format_class


def get_args():
    parser = argparse.ArgumentParser(description="Extract all classes and method names from a java source file")
    parser.add_argument("-j", "--java-file", help="Path to java source file")
    parser.add_argument("-f", "--format", help="Format to print the class structure in",
                        choices=["dot", "txt"], default="txt")
    args = parser.parse_args()

    return args


def main():
    args = get_args()
    java_file = os.path.abspath(args.java_file)
    print_format = args.format

    if print_format == "dot":
        a = format_class_dot_node(java_file)
    elif print_format == "txt":
        a = format_class(java_file)
    else:
        sys.exit()

    for i in a:
        print(i)


if __name__ == '__main__':
    main()
