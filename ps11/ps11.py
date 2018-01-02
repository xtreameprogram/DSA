# 6.00 Problem Set 11
#
# ps11.py
#
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string, itertools
from graph import Digraph, Edge, Node

#
# Problem 2: Building up the Campus Map
#
# Write a couple of sentences describing how you will model the
# problem as a graph)
#

def load_map(mapFilename):
    print "Loading map from file..."
    dataFile = open(mapFilename, 'r')

    digraph = Digraph()
    # e = Edge('36', '70','0')
    # digraph.addNode(Node('32', [e]))

    for line in dataFile:
        c = line.rstrip().split(' ')
        edge = Edge(c[1], c[2], c[3])
        if digraph.getNode(c[0]) is None: 
            n = Node(c[0], [edge])
            digraph.addNode(n)
        else:
            digraph.getNode(c[0]).addEdge(edge)
    return digraph


#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and the constraints
#

def areConnected(digraph, sub):
    for i in xrange(0, len(sub) - 1):
        if not digraph.getNode(sub[i]).connected(sub[i+1]):
            return False
    return True

def distGood(maxt, maxo, sub):
    st = 0
    so = 0
    for k in xrange(0, len(sub) - 1):
        n = digraph.getNode(sub[k]).getEdge(sub[k + 1])
        st += int(n.getTotalLength())
        so += int(n.getOutsideLength())
    return maxt >= st and maxo >= so


def isComplete(start, end, subset):
    if len(subset) > 0:
        # print start, subset[0]
        # print end, subset[-1:][0]
        return start == subset[0] and subset[-1:][0] == end
    return False

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):
    if start == end:
        return end
    stuff = digraph.getNames()
    for L in xrange(0, len(stuff)+1):
        for subset in itertools.permutations(stuff, L):
            if areConnected(digraph, subset) and distGood(maxTotalDist, maxDistOutdoors, subset) and isComplete(start, end, subset):
                return subset
    return "No Path Found"


#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFSUnder(digraph, current, end, maxTotalDist, maxDistOutdoors, edge, visited = []):
    if current in visited:
        return False, ""

    if current == end:
        return True, [current]


    currentNode = digraph.getNode(current)
    edges = currentNode.getEdges()

    for e in edges:
        if e.getDestination() == end:
            result, add = directedDFSUnder(digraph, e.getDestination(), end, maxTotalDist, maxDistOutdoors, edge, visited)
            if result:
                return True, add + [current]

    if len(edges) == 0:
        return False, ""

    visited.append(current)

    for edge in edges:
        if not (int(edge.getTotalLength()) > maxTotalDist or int(edge.getOutsideLength()) > maxDistOutdoors):
            result, add = directedDFSUnder(digraph, edge.getDestination(), end, maxTotalDist, maxDistOutdoors, edge, visited)
            if result:
                return True, add + [current]
    
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    t, ret = directedDFSUnder(digraph, start, end, maxTotalDist, maxDistOutdoors, None)
    return list(reversed(ret))




    # if current in visited:
    #     return (9999999, 9999999)

    # if current == end:
    #     return (edge.getTotalLength(), edge.getOutsideLength())
    
    # currentNode = digraph.getNode(current)
    # visited.append(current)
    # edges = currentNode.getEdges()
    # lst = None
    # for e in edges:
    #     if not (e.getTotalLength() > maxTotalDist or e.getOutsideLength() > maxDistOutdoors):
    #         y, l = directedDFS(digraph, e.getDestination().getName(), end, maxTotalDist - e.getTotalLength(), maxDistOutdoors - e.getOutsideLength(), e, visited)
    #         if lst is None:
    #             lst = (y, l)
    #         elif y < lst[0]:
    #             lst = (y,l)

    # return lst
    

    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """



if __name__ == '__main__':
    # Test cases
    digraph = load_map("mit_map.txt")

    LARGE_DIST = 1000000

    # Test case 1
    print "---------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
    brutePath1 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
    dfsPath1 = directedDFS(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath1
    print "Brute-force: ", brutePath1
    print "DFS: ", dfsPath1

    # Test case 2
    print "---------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
    brutePath2 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, 0)
    dfsPath2 = directedDFS(digraph, '32', '56', LARGE_DIST, 0)
    print "Expected: ", expectedPath2
    print "Brute-force: ", brutePath2
    print "DFS: ", dfsPath2

    # Test case 3
    print "---------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
    brutePath3 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
    dfsPath3 = directedDFS(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath3
    print "Brute-force: ", brutePath3
    print "DFS: ", dfsPath3

    # Test case 4
    print "---------------"
    print "Test case 4:"
    print "Find the shortest-path from Building 2 to 9 without going outdoors"
    expectedPath4 = ['2', '4', '10', '13', '9']
    brutePath4 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, 0)
    dfsPath4 = directedDFS(digraph, '2', '9', LARGE_DIST, 0)
    print "Expected: ", expectedPath4
    print "Brute-force: ", brutePath4
    print "DFS: ", dfsPath4

    # Test case 5
    print "---------------"
    print "Test case 5:"
    print "Find the shortest-path from Building 1 to 32"
    expectedPath5 = ['1', '4', '12', '32']
    brutePath5 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
    dfsPath5 = directedDFS(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath5
    print "Brute-force: ", brutePath5
    print "DFS: ", dfsPath5

    # Test case 6
    print "---------------"
    print "Test case 6:"
    print "Find the shortest-path from Building 1 to 32 without going outdoors"
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    brutePath6 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, 0)
    dfsPath6 = directedDFS(digraph, '1', '32', LARGE_DIST, 0)
    print "Expected: ", expectedPath6
    print "Brute-force: ", brutePath6
    print "DFS: ", dfsPath6

    # Test case 7
    print "---------------"
    print "Test case 7:"
    print "Find the shortest-path from Building 8 to 50 without going outdoors"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(digraph, '8', '50', LARGE_DIST, 0)
    except ValueError:
        bruteRaisedErr = 'Yes'      
    try:
        directedDFS(digraph, '8', '50', LARGE_DIST, 0)
    except ValueError:
        dfsRaisedErr = 'Yes'        
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

    # Test case 8
    print "---------------"
    print "Test case 8:"
    print "Find the shortest-path from Building 10 to 32 without walking"
    print "more than 100 meters in total"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(digraph, '10', '32', 100, LARGE_DIST)
    except ValueError:
        bruteRaisedErr = 'Yes'
   
    try:
        directedDFS(digraph, '10', '32', 100, LARGE_DIST)
    except ValueError:
        dfsRaisedErr = 'Yes'        
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

