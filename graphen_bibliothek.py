#!/usr/bin/env python3

"""Graph modelling for DSA 2018.

This file contains data structures to represent graphs (along with nodes and
edges) in Python.
"""
class ColorMixin:
    """Mixin for a color property."""
    def __init__(self, *, color, **kwargs):
        """Constructor."""
        super().__init__(**kwargs)
        self.color = color

class WeightMixin:
    """Mixin for a weight property."""
    def __init__(self, *, weight, **kwargs):
        """Constructor."""
        super().__init__(**kwargs)
        self.weight = weight

class BaseNode:
    """Base class for nodes.

    All node classes must inherit this class.
    """
    def __init__(self, *, name, **kwargs):
        """Constructor."""
        super().__init__(**kwargs)
        self.name = name

    def __repr__(self):
        """Convert to a printable representation."""
        data = vars(self)
        if len(data) == 1:
            return data['name']
        else:
            return "{}: {}".format(data['name'], {k: v for k, v in data.items()
                                                  if k != 'name'})

class ColoredNode(ColorMixin, BaseNode):
    """Nodes with a color property.

    This is an example of mixin usage.
    """
    pass


class BaseEdge:
    """Base class for edges.

    All edge classes must inherit this class.
    """
    def __init__(self, *, vertices, **kwargs):
        """Constructor."""
        super().__init__(**kwargs)
        self.vertices = vertices

    def __repr__(self):
        """Convert to a printable representation."""
        data = vars(self)
        if isinstance(data['vertices'], frozenset):
            ident = "{{{}}}".format(", ".join(sorted(data['vertices'])))
        else:
            ident = "({{}})".format(", ".join(sorted(data['vertices'])))
        if len(data) == 1:
            return ident
        else:
            return "{}: {}".format(ident, {k: v for k, v in data.items()
                                           if k != 'vertices'})

class WeightedEdge(WeightMixin, BaseEdge):
    """Edges with a weight property.

    This is an example of mixin usage.
    """
    pass

class Graph():
    """Central class to model a graph.

    This provides most of the functionality. It can represent a quite
    diverse set of graphs.
    """
    def __init__(self, directed=False, loops=False, nodecls=BaseNode,
                 edgecls=BaseEdge):
        """Constructor.

        The arguments are as follows:
        * directed: True if the edges of the graph should have an orientation
        * loops: True if the two vertices of an edge are allowed to coincide
        * nodecls: class of the nodes used by this graph (allows additional
                   properties if customized)
        * edgecls: class of the edges used by this graph (allows additional
                   properties if customized)
        """
        self.nodes = {}
        self.edges = {}
        self.nodecls = nodecls
        self.edgecls = edgecls
        self.directed = directed
        self.loops = loops
        
    def __eq__(self,other):
        for node in self.nodes:
            if node not in other.nodes:
                return False
        for node in other.nodes:
            if node not in self.nodes:
                return False
        for edge in self.edges:
            if edge not in other.edges:
                return False
        for edge in other.edges:
            if edge not in self.edges:
                return False
        return True
        
    def make_node(self, name, **kwargs):
        """Create a new node.

        The parameter name has to uniquely identify the node.

        Returns the newly instantiated node.
        """
        if name in self.nodes:
            raise ValueError("There already exists a node with this name.")
        node = self.nodecls(name=name, **kwargs)
        self.nodes[name] = node
        return node

    def make_edge(self, start, end, **kwargs):
        """Create a new edge.

        The parameters start and end are the vertices of the edge and the
        order is only important if the graph is directed. They can either be
        the names of the nodes or the actual node objects.

        Returns the newly instantiated edge.
        """
        if isinstance(start, BaseNode):
            start = start.name
        if isinstance(end, BaseNode):
            end = end.name
        if not self.loops and start == end:
            raise ValueError("No loops allowed.")
        if start not in self.nodes or end not in self.nodes:
            raise ValueError("Nonexistent node specified.")
        if self.directed:
            vertices = (start, end)
        else:
            vertices = frozenset((start, end))
        if vertices in self.edges:
            raise ValueError("There exists an edge between these nodes.")

        new = self.edgecls(vertices=vertices, **kwargs)
        self.edges[vertices] = new
        return new

    def get_edge(self, start, end):
        """Helper to determine if an edge exists."""
        if isinstance(start, BaseNode):
            start = start.name
        if isinstance(end, BaseNode):
            end = end.name
        if self.directed:
            vertices = (start, end)
        else:
            vertices = frozenset((start, end))
        return vertices in self.edges

    def edge_to_vertices(self, edge):
        """Helper to extract the vertices of an edge.

        This is trickier than expected since we have to cover all possible
        scenarios.
        """
        if not isinstance(edge, BaseEdge):
            edge = self.edges[edge]
        if len(edge.vertices) == 2:
            start, end = tuple(edge.vertices)
        else:
            start = next(iter(edge.vertices))
            end = start
        return start, end

    def remove_node(self, name):
        """Delete a node.

        This also deletes all edges having this node as vertex.

        The parameter can either be the name of the node or the actual node
        object.
        """
        if isinstance(name, BaseNode):
            name = name.name
        if name not in self.nodes:
            raise ValueError("No node with this name.")

        for edge in tuple(self.edges):
            if name in edge:
                start, end = self.edge_to_vertices(edge)
                del self.edges[edge]
        del self.nodes[name]

    def remove_edge(self, start, end=None):
        """Delete an edge.

        The parameter start and end can either be the names of the vertices
        or the node objects describing the vertices. Additionally if the
        parameter end is omitted, start can be an edge object designating
        the edge to be expunged.
        """
        if end is None:
            if isinstance(start, BaseEdge):
                start, end = self.edge_to_vertices(start)
            else:
                raise ValueError("An edge must be given as sole argument.")

        if isinstance(start, BaseNode):
            start = start.name
        if isinstance(end, BaseNode):
            end = end.name
        if self.directed:
            vertices = (start, end)
        else:
            vertices = frozenset((start, end))
        if vertices not in self.edges:
            raise ValueError("No edge between these nodes.")

        del self.edges[vertices]

    def __repr__(self):
        """Convert to a printable representation."""
        nodes = "({})".format(", ".join(repr(self.nodes[n])
                                        for n in sorted(self.nodes)))
        edges = "({})".format(", ".join(repr(self.edges[e])
                                        for e in sorted(self.edges)))
        return "Graph(nodes={}, edges={})".format(nodes, edges)

###hinzugefügt
def neighbors(graph, node):
    neighbour_list=[]
    for node_name in graph.nodes:
        if graph.get_edge(node_name, node):
            neighbour_list.append(node_name)
    return neighbour_list


if __name__ == "__main__":
    g = Graph()
    a = g.make_node('a')
    b = g.make_node('b')
    c = g.make_node('c')
    e = g.make_edge('a', 'b')
    f = g.make_edge(a, c)
    print(a)
    print(e)
    print(g)
    g.remove_edge(a, c)
    g.remove_node(b)
    print(g)
