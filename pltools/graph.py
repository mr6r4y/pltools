import graphviz as gv
import subprocess as sp
import collections
import tempfile
import os


def struct_to_label(s):
    if isinstance(s, tuple):
        sub_id, body = s
        if isinstance(body, basestring):
            return '<%s> %s' % (sub_id, body)
        elif isinstance(body, collections.Iterable):
            b = " | ".join([struct_to_label(i) for i in body])
            return '{<%s> %s | {%s}}' % (sub_id, sub_id, b)
    elif isinstance(s, basestring):
        return '<%s> %s' % (s, s)


def arrow(g, edges):
    for i in range(len(edges) - 1):
        if isinstance(edges[i + 1], basestring):
            g.edge(edges[i], edges[i + 1])
        elif isinstance(edges[i + 1], collections.Iterable):
            for j in edges[i + 1]:
                g.edge(edges[i], j)


def xdot(g):
    f, fname = tempfile.mkstemp('.dot')
    g.save(fname)
    p = ['xdot', fname]
    a = sp.Popen(p)
    a.wait()
    os.unlink(fname)
