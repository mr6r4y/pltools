import graphviz as gv
from pltools.graph import struct_to_label, xdot


TestStructA = ("TestStructA",
              [("a", "TestA"), ("b", "TestB"), ("c", "TestC")])
TestStructB = ("TestStructB",
              [TestStructA, ("d", "TestD")])


def main():
    d_structs = gv.Digraph(name="cluster_structs")
    d_structs.attr("graph", label="structs")
    d_structs.node_attr["shape"] = "record"

    d_structs.node("s1", label=struct_to_label(TestStructA))
    d_structs.node("s2", label=struct_to_label(TestStructA))
    d_structs.node("s3", label=struct_to_label(TestStructA))
    d_structs.node("s4", label=struct_to_label(TestStructB))

    d_structs.edge("s1:a", "s2:b")
    d_structs.edge("s3", "s2")
    d_structs.edge("s4:a", "s1")


    d = gv.Digraph()
    # d.graph_attr["splines"] = "ortho"
    d.node_attr["shape"] = "box"
    d.subgraph(d_structs)

    # print(d)
    xdot(d)


if __name__ == '__main__':
    main()