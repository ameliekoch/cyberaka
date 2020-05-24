#! /usr/bin/python3
import matplotlib.pyplot as plt
import tsplib95
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import copy

def isCyclicUtil(G, v, visited, parent):
    visited[v] = True
    for i in G.neighbors(v): 
        # If the node is not visited then recurse on it 
        if  visited[i]==False :  
            if(isCyclicUtil(G,i,visited,v)): 
                return True
        # If an adjacent vertex is visited and not parent of current vertex, 
        # then there is a cycle 
        elif  parent!=i:
            return True
    return False


def isCyclic(G): #gleich wie Tiefensuche, im Idealfall O(V+E)
        visited = {}
        for node in G.nodes():
            visited[node] = False

        for i in G.nodes(): 
            if visited[i] ==False:
                if(isCyclicUtil(G, i,visited,list(G.nodes())[-1]))== True: 
                    return True

        return False


def minspantree(G):
    nodes = set(G.nodes)
    edges = list(G.edges)
    edges.sort(key = lambda edge: G.edges[edge]["weight"]) # O(E log E)
    edges.reverse()
    colorededges = set([])
    while len(colorededges) < len(nodes)-1:
        edge = edges.pop() # lowest weight
        if not isCyclic(nx.Graph(list(colorededges | set([edge])))): # isCyclic: <= O(V + E)
            colorededges.add(edge)
    result = nx.Graph(list(colorededges))
    return result

def oddsubgraph(T, G): # T is the spanning tree, G is the start graph
    newnodes = []
    for node in T.nodes:
        if T.degree[node] % 2 == 1:
            newnodes.append(node)

    return G.subgraph(newnodes)

def perfectmatching(O):
    nodes = list(O.nodes)
    edges = list(O.edges)
    edges.sort(key = lambda edge: O.edges[edge]["weight"]) # O(E log E)
    edges.reverse()
    colorededges = set([])
    while len(colorededges) < len(nodes)/2:
        edge = edges.pop() # lowest weight
        test = nx.Graph(list(colorededges | set([edge])))
        if test.degree[edge[0]] < 2 and test.degree[edge[1]] < 2:
            colorededges.add(edge)
    result = nx.Graph(list(colorededges))

    return result

def flip(edge):
    return (edge[1], edge[0], edge[2])

def possibleedge(G, node, usededges): # returns an edge that is adjacent to node, but not in usededges
    for edge in G.edges:
        if node == edge[0] or node == edge[1]:
            if edge not in usededges and flip(edge) not in usededges:
                return edge
    print("no edge found, error with node: ", node, "rerunning:")
    for edge in G.edges:
        if node == edge[0] or node == edge[1]:
            print(edge)
            if edge not in usededges and flip(edge) not in usededges:
                return edge    

def getothernode(edge, node):
    if edge[0] == node:
        return edge[1]
    else:
        return edge[0]

def find_u(G, usededges, tour):
    for node in tour:
        for edge in G.edges:
            if node == edge[0] or node == edge[1]:
                if edge not in usededges and flip(edge) not in usededges:
                    return node

def insertnodestour(tour, newtour, u):
    rettour1 = []
    rettour2 = []
    onetwo = True
    for node in tour:
        if node != u and onetwo:
            rettour1.append(node)
        elif node == u and onetwo:
            onetwo = False
        else:
            rettour2.append(node)

    for node in newtour:
        rettour1.append(node)
    for node in rettour2:
        rettour1.append(node)
    return rettour1

def insertedgestour(usededges, newedgetour, u):
    rettour1 = []
    rettour2 = []
    onetwo = True
    for edge in usededges:
        if u not in edge and onetwo:
            rettour1.append(edge)
        elif u in edge and onetwo:
            rettour1.append(edge)
            onetwo = False
        else:
            rettour2.append(edge)
    for edge in newedgetour:
        rettour1.append(edge)

    for edge in rettour2:
        rettour1.append(edge)
    return rettour1

def EulerianCircle(G):
    nodes = list(G.nodes)
    edges = list(G.edges)
    node = nodes[0]
    usededges = []
    tour = [node]
    cycle = False
    while not cycle:
        edge = possibleedge(G, node, usededges)
        usededges.append(edge)
        node = getothernode(edge, node)
        tour.append(node)
        if tour[-1] == tour[0]:
            cycle = True
    #print("first circle: ", usededges)

    while len(usededges) < len(edges):
        u = find_u(G, usededges, tour)
        #print("next u: ", u)
        #start tour at u
        newtour = [u]
        newedgetour = []
        cycle = False
        node = u
        usededges2 = copy.deepcopy(usededges)
        while not cycle:
            edge = possibleedge(G, node, usededges2)
            usededges2.append(edge)
            newedgetour.append(edge)
            node = getothernode(edge, node)
            newtour.append(node)
            if newtour[-1] == newtour[0]:
                cycle = True
        # and insert new tour into old tour
        tour = insertnodestour(tour, newtour, u)
        usededges = insertedgestour(usededges, newedgetour, u)
        #print("another circle: ", newedgetour)
        #print("total tour: ", tour)
    return usededges


def HamiltonianCircle(eulerian):
    #first find out the first and last node, this node can be visited twice
    firstnodes = [eulerian[0][0], eulerian[0][1]] 
    lastnodes = [eulerian[-1][0], eulerian[-1][1]]
    if firstnodes[0] in lastnodes:
        node = firstnodes[0]
    else:
        node = firstnodes[1]
    visitednodes = [node]
    for edge in eulerian:
        node = getothernode(edge, node) # get next node that is visited
        if node not in visitednodes:
            visitednodes.append(node)
    #create way from visitednodes
    hamiltonian = []
    node1 = visitednodes[0]
    node2 = visitednodes[0]
    for node in visitednodes[1:]:
        node1 = node2
        node2 = node
        hamiltonian.append((node1, node2))
    hamiltonian.append((node2, visitednodes[0]))
    return hamiltonian

def weight(hamiltonian, G):
    weight = 0
    for edge in hamiltonian:
        weight += G.edges[edge]["weight"]
    return weight

def preproc(G):
    G.remove_edges_from(nx.selfloop_edges(G))


def draw(G, hamiltonian):
    pos = nx.circular_layout(G)

    # draw it
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color='k', width=0.5) # show all edges, thin lines
    nx.draw_networkx_edges(G, pos, edgelist=hamiltonian, edge_color='b', width=2) # highlight elist

    plt.show()



def christofides(path):
    problem = tsplib95.load(path)
    G = problem.get_graph()
    preproc(G)

    T = minspantree(G)

    O = oddsubgraph(T, G)

    M = perfectmatching(O)

    H = nx.MultiGraph()
    H.add_edges_from(T.edges)
    H.add_edges_from(M.edges)

    print(H.edges)
    nx.draw_networkx(H)
    #plt.show()
    eulerian = EulerianCircle(H)

    hamiltonian = HamiltonianCircle(eulerian)
    #draw(G, hamiltonian)
    return weight(hamiltonian, G)


print(christofides("tsplib/a280.tsp"))
#print(christofides(sys.argv[1]))