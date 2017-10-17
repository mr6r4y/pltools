import tempfile
import os

import subprocess as sp
import collections
from cgi import escape


def esc(s):
    return escape(s).replace("\\", "\\\\").replace("\n","\\l")


def struct_to_label(s):
    if isinstance(s, tuple):
        sub_id, body = s
        if isinstance(body, basestring):
            return '<%s> %s' % (sub_id, esc(body))
        elif isinstance(body, collections.Iterable):
            b = " | ".join([struct_to_label(i) for i in body])
            return '{<%s> %s | {%s}}' % (sub_id, sub_id, b)
    elif isinstance(s, basestring):
        return '<%s> %s' % (esc(s), esc(s))


def arrow(g, edges):
    for i in range(len(edges) - 1):
        if isinstance(edges[i + 1], basestring):
            g.edge(esc(edges[i]), esc(edges[i + 1]))
        elif isinstance(edges[i + 1], collections.Iterable):
            for j in edges[i + 1]:
                g.edge(esc(edges[i]), esc(j))


def nodes(g, nodes):
    for n in nodes:
        if isinstance(n, basestring):
            g.node(name=esc(n))
        elif isinstance(n, tuple):
            g.node(name=esc(n[0]), label=esc(n[1]))


def xdot(g):
    f, fname = tempfile.mkstemp('.dot')
    g.save(fname)
    p = ['xdot', fname]
    a = sp.Popen(p)
    a.wait()
    os.unlink(fname)
