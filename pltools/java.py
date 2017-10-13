import os
import re
import subprocess as sp
import json
import graphviz as gz


__all__ = [
    "ProjectStructure",
    "dump_project_structure",
    "project_structure_dot"
]


class ProjectStructure(object):

    def __init__(self):
        self.project_struct = {}

    def _parse_src_file(self, fl):
        d = fl.read()
        package_name = self._parse_package_name(d)
        classes = self._parse_classes(d)

        return package_name, classes

    def _parse_package_name(self, data):
        a = re.search("package (.*);", data)

        return a.group(1) if a else None

    def _parse_classes(self, data):
        # Currently for the sake of rapid development
        # I use regex for parsing the classes in a file.
        # Assuming that there is a 1 class per file we
        # should not have problems for now.
        # However this approach breaks easily and a
        # context-free parser should be used. Currently some
        # time will be invested in Antlr4.

        c = re.search("^(public |private |protected )?class ([a-zA-Z_]+).*?{(.*)}",
                      data, re.MULTILINE | re.DOTALL)
        if c is None:
            return {}

        class_name = c.group(2)

        m = re.findall("^[\s]*(?:public |private |protected )[^@]*?([a-zA-Z_]+)[\s]*\(.*?\)[\s]*{",
                       c.group(3), re.MULTILINE)

        return {class_name: m}

    def _merge(self, item, pool):
        package, classes = item
        if package in pool:
            for k, v in classes.items():
                pool[package][k] = v
        else:
            pool[package] = classes

    def _parse(self, java_files):
        for f in java_files:
            try:
                with open(f, "r") as fl:
                    package, classes = self._parse_src_file(fl)
                    self._merge((package, classes), self.project_struct)
            except Exception:
                print f

    def project(self, path):
        old_cwd = os.path.abspath(os.getcwd())
        os.chdir(path)

        java_files = map(lambda a: a.strip(),
                         sp.Popen(["find", ".", "-iname", "*.java"],
                                  stdout=sp.PIPE).communicate()[0].split("\n"))
        self._parse(java_files)

        os.chdir(old_cwd)


def dump_project_structure(path, dump_file):
    p = ProjectStructure()
    p.project(path)
    json.dump(p.project_struct, open(dump_file, "w"), indent=2, sort_keys=True)


def project_structure_dot(project_structure, dot_file, edges=None):
    def _cl_to_pkg_map(proj_struct):
        cl_struct = {}
        for pkg in proj_struct.keys():
            for cl in proj_struct[pkg].keys():
                cl_struct[cl] = pkg

        return cl_struct

    def _edges_to_proj_struct(proj_struct, edges):
        cl_struct = _cl_to_pkg_map(proj_struct)
        edges_struct = {}
        for (cl1, mthd1), (cl2, mthd2) in edges:
            pkg1 = cl_struct.get(cl1, '-')
            pkg2 = cl_struct.get(cl2, '-')

            if pkg1 in edges_struct:
                if cl1 in edges_struct[pkg1]:
                    if mthd1 not in edges_struct[pkg1][cl1]:
                        edges_struct[pkg1][cl1].append(mthd1)
                else:
                    edges_struct[pkg1][cl1] = [mthd1]
            else:
                edges_struct[pkg1] = {cl1: [mthd1]}

            if pkg2 in edges_struct:
                if cl2 in edges_struct[pkg2]:
                    if mthd2 not in edges_struct[pkg2][cl2]:
                        edges_struct[pkg2][cl2].append(mthd2)
                else:
                    edges_struct[pkg2][cl2] = [mthd2]
            else:
                edges_struct[pkg2] = {cl2: [mthd2]}
        return edges_struct

    def _format_edges(proj_struct, edges):
        cl_struct = _cl_to_pkg_map(proj_struct)

        for edge in edges:
            cl1, method1 = edge[0]
            try:
                cl2, method2 = edge[1]
            except Exception:
                print edge
            pkg1 = cl_struct.get(cl1, '-')
            pkg2 = cl_struct.get(cl2, '-')

            tail_name = "%s:%s" % (_get_node_id(pkg1, cl1), method1)
            head_name = "%s:%s" % (_get_node_id(pkg2, cl2), method2)

            yield tail_name, head_name

    def _format_methods_to_label(cl, methods):
        return "%s | {%s}" % (cl, " | ".join(methods))

    def _get_node_id(pkg, cl):
        return "%s.%s" % (pkg, cl)

    def _filter_node(pkg, cl, edges):
        pass

    d = gz.Digraph()
    d.node_attr["shape"] = "record"
    d.graph_attr["splines"] = "ortho"

    if edges is not None:
        edge_struct = _edges_to_proj_struct(project_structure, edges)
        for pkg in edge_struct.keys():
            # prefix 'cluster' is important for visibility
            pkg_id = "cluster_" + pkg
            dd = gz.Digraph(name=pkg_id)
            dd.attr(label=pkg)
            dd.attr(style="filled")
            dd.attr(color="lightgrey")

            for cl in edge_struct[pkg].keys():
                node_id = _get_node_id(pkg, cl)
                l = _format_methods_to_label(cl, edge_struct[pkg][cl])
                dd.node(node_id, label=l)

            d.subgraph(dd)
    else:
        for pkg in project_structure.keys():
            # prefix 'cluster' is important for visibility
            pkg_id = "cluster_" + pkg
            dd = gz.Digraph(name=pkg_id)
            dd.attr(label=pkg)
            dd.attr(style="filled")
            dd.attr(color="lightgrey")

            for cl in project_structure[pkg].keys():
                node_id = _get_node_id(pkg, cl)
                l = _format_methods_to_label(cl, project_structure[pkg][cl])
                dd.node(node_id, label=l)

            d.subgraph(dd)

    if edges is not None:
        e = [i for i in _format_edges(project_structure, edges)]
        d.edges(e)

    d.save(dot_file)


# Cluster on Class not on package
def project_structure_2_dot(project_structure, dot_file, edges=None):
    def _cl_to_pkg_map(proj_struct):
        cl_struct = {}
        for pkg in proj_struct.keys():
            for cl in proj_struct[pkg].keys():
                cl_struct[cl] = pkg

        return cl_struct

    def _edges_to_proj_struct(proj_struct, edges):
        cl_struct = _cl_to_pkg_map(proj_struct)
        edges_struct = {}
        for (cl1, mthd1), (cl2, mthd2) in edges:
            pkg1 = cl_struct.get(cl1, '-')
            pkg2 = cl_struct.get(cl2, '-')

            if pkg1 in edges_struct:
                if cl1 in edges_struct[pkg1]:
                    if mthd1 not in edges_struct[pkg1][cl1]:
                        edges_struct[pkg1][cl1].append(mthd1)
                else:
                    edges_struct[pkg1][cl1] = [mthd1]
            else:
                edges_struct[pkg1] = {cl1: [mthd1]}

            if pkg2 in edges_struct:
                if cl2 in edges_struct[pkg2]:
                    if mthd2 not in edges_struct[pkg2][cl2]:
                        edges_struct[pkg2][cl2].append(mthd2)
                else:
                    edges_struct[pkg2][cl2] = [mthd2]
            else:
                edges_struct[pkg2] = {cl2: [mthd2]}
        return edges_struct

    def _format_edges(proj_struct, edges):
        cl_struct = _cl_to_pkg_map(proj_struct)

        for edge in edges:
            cl1, method1 = edge[0]
            cl2, method2 = edge[1]

            tail_name = _get_node_id(cl1, method1)
            head_name = _get_node_id(cl2, method2)

            yield tail_name, head_name

    def _format_methods_to_label(cl, methods):
        return "%s | {%s}" % (cl, " | ".join(methods))

    def _get_node_id(cl, m):
        return "%s.%s" % (cl, m)

    def _filter_node(pkg, cl, edges):
        pass

    d = gz.Digraph()
    d.node_attr["shape"] = "record"
    d.graph_attr["splines"] = "ortho"
    d.attr(rankdir="LR")

    if edges is not None:
        edge_struct = _edges_to_proj_struct(project_structure, edges)
        for pkg in edge_struct.keys():
            for cl in edge_struct[pkg].keys():
                cl_id = "cluster_" + cl
                dd = gz.Digraph(name=cl_id)
                dd.attr(label=cl)
                dd.attr(style="filled")
                dd.attr(color="lightgrey")

                for m in edge_struct[pkg][cl]:
                    node_id = _get_node_id(cl, m)
                    l = m
                    dd.node(node_id, label=l)

                d.subgraph(dd)
    else:
        for pkg in project_structure.keys():
            for cl in project_structure[pkg].keys():
                cl_id = "cluster_" + cl
                dd = gz.Digraph(name=cl_id)
                dd.attr(label=cl)
                dd.attr(style="filled")
                dd.attr(color="lightgrey")

                for m in project_structure[pkg][cl]:
                    node_id = _get_node_id(cl, m)
                    l = m
                    dd.node(node_id, label=l)

                d.subgraph(dd)

    if edges is not None:
        e = [i for i in _format_edges(project_structure, edges)]
        d.edges(e)

    d.save(dot_file)
