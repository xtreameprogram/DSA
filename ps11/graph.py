class Node(object):
    def __init__(self, name, edges = []):
        self.name = str(name)
        self.edges = edges

    def getName(self):
        return self.name

    def __str__(self):
        ret = self.name
        for e in self.edges:
            ret += '\n->' + e.getDestination()
        return ret

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def addEdge(self, edge):
        self.edges.append(edge)
    
    def getEdges(self):
        return self.edges

    def connected(self, other):
        for e in self.edges:
            if e.getDestination() == other:
                return True
        return False

    def getEdge(self, n):
        for r in self.edges:
            if r == n:
                return r
        return None


class Edge(object):

    def __init__(self, dest, total, outside):
        self.dest = dest
        self.total = total
        self.outside = outside

    def getTotalLength(self):
        return self.total

    def getOutsideLength(self):
        return self.outside

    def getDestination(self):
        return self.dest

    def __eq__(self, other):
        return self.dest == other



class Digraph(object):
    def __init__(self, nodes = []):
        self.nodes = nodes

    def addNode(self, node):
        self.nodes.append(node)
    
    def getNode(self, name):
        for n in self.nodes:
            if n.getName() == name:
                return n
        return None

    def __str__(self):
        ret = ""
        for n in self.nodes:
            ret += "\n" + n.getName()
            for e in n.getEdges():
                ret += "\n->" + e.getDestination()

        return ret

    def getNames(self):
        ret = []
        for k in self.nodes:
            ret.append(k.getName())
        return ret

    # def __init__(self):
    #     self.nodes = set([])
    #     self.edges = {}

    # def addNode(self, node):
    #     if node in self.nodes:
    #         raise ValueError('Duplicate node')
    #     else:
    #         self.nodes.add(node)
    #         self.edges[node] = []

    # def addEdge(self, edge):
    #     src = edge.getSource()
    #     dest = edge.getDestination()
    #     if not (src in self.nodes and dest in self.nodes):
    #         raise ValueError('Node not in graph')
    #     self.edges[src].append(dest)

    # def childrenOf(self, node):
    #     return self.edges[node]

    # def hasNode(self, node):
    #     return node in self.nodes

    # def __str__(self):
    #     res = ''
    #     for k in self.edges:
    #         for d in self.edges[k]:
    #             res = res + str(k) + '->' + str(d) + '\n'
    #     return res[:-1]



			