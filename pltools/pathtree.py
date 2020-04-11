import os
import sys
import argparse
import re
import graphviz as gv

from .graph import list_to_label


class PathTree(object):
    def __init__(self):
        self.tree = {"dirs": {}, "files": set()}
        self.graph = None
        self._unique_id = 0

        self.separate_file_nodes = False

    @classmethod
    def _add(cls, node, path, filename):
        if path[0] not in node["dirs"]:
            node["dirs"][path[0]] = {"dirs": {}, "files": set()}
        if len(path) > 1:
            cls._add(node["dirs"][path[0]], path[1:], filename)
        elif len(path) == 1:
            node["dirs"][path[0]]["files"].add(filename)

    def add(self, path, filename):
        self._add(self.tree, path, filename)

    @classmethod
    def _init_graph(cls):
        g = gv.Digraph()
        g.graph_attr["splines"] = "ortho"
        g.graph_attr["rankdir"] = "LR"
        g.node_attr["shape"] = "record"

        return g

    def get_id(self):
        v = self._unique_id
        self._unique_id += 1
        return v

    def _compress_dirs(self, node, parent):
        if len(node["dirs"]) == 1 and len(node["files"]) == 0:
            for directory in node["dirs"]:
                directory_id = "%s_%i" % (directory, self.get_id())
                if not parent[0]:
                    parent = (directory_id, "")
                new_directory = (parent[1] + "/" + directory)
                return self._compress_dirs(node["dirs"][directory], (parent[0], new_directory))
        else:
            return (node, parent)

    def _connect_nodes(self, node, parent):
        node, parent = self._compress_dirs(node, parent)

        if self.separate_file_nodes:
            for fl in node["files"]:
                file_id = "%s_%i" % (fl, self.get_id())
                self.graph.node(file_id, label=fl)
                if parent[0]:
                    self.graph.edge(parent[0], file_id)
        else:
            files_id = "files_%i" % self.get_id()

            if len(node["files"]) > 0:
                self.graph.node(files_id, shape="none", margin="0", label=list_to_label(node["files"]))

            if parent[0] and len(node["files"]) > 0:
                self.graph.edge(parent[0], files_id)

        for directory in node["dirs"]:
            directory_id = "%s_%i" % (directory, self.get_id())
            new_node, new_directory = self._compress_dirs(node["dirs"][directory], (directory_id, directory))
            self.graph.node(new_directory[0], label=new_directory[1])
            if parent[0]:
                self.graph.edge(parent[0], directory_id)

            self._connect_nodes(new_node, new_directory)

    def generate_graph(self, separate_file_nodes):
        self.separate_file_nodes = separate_file_nodes
        self.graph = self._init_graph()
        self._connect_nodes(self.tree, (None, None))

    def print_dot(self):
        print(self.graph)


def is_excluded(excluded, root):
    return any(map(lambda a: a.strip("/") in root.split("/"), excluded))


def get_args():
    parser = argparse.ArgumentParser(description="Parses strings of source code from crash dump and generates a source tree")
    parser.add_argument("-f", "--strings-file", help="File containing strings of source names")
    parser.add_argument("-d", "--directory", help="Build graph dot file from a directory tree instead of a file with path collection")
    parser.add_argument("-s", "--separate-file-nodes", action="store_true", default=False,
                        help="If set, the files are generated as separate nodes not as record struct")

    args = parser.parse_args()
    return args


def main():
    args = get_args()

    pt = PathTree()

    if args.strings_file:
        line_regex = "\\.\\./([a-zA-Z]+/.*)"
        with open(args.strings_file, "r") as str_f:
            for line in str_f:
                m = re.search(line_regex, line.strip())
                if not m:
                    continue
                path_str = m.group(1)
                filename = os.path.basename(path_str)
                path_str = os.path.dirname(path_str)
                path = [p for p in path_str.split("/") if p.lower() not in (".",)]
                # path = path_str.split("/")
                # path = [p for p in path_str.split("/") if p.lower() not in (".", "code", "src", "inc")]
                path = tuple(path)

                pt.add(path, filename)
    elif args.directory:
        excluded = [".git"]

        for root, dirs, files in os.walk(args.directory):
            if not is_excluded(excluded, root):
                for filename in files:
                    path = tuple(root.split(args.directory)[1].split("/"))
                    pt.add(path, filename)
    else:
        print("You must supply --strings-file or --directory")
        return

    pt.generate_graph(args.separate_file_nodes)
    pt.print_dot()


if __name__ == "__main__":
    main()
