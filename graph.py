from copy import deepcopy
class graph:
    
    nodes=[]
    numOfNodes=0
    shortestPath=[]
    
    def __init__ (self):
        return
    
    #Add a node to the graph. The input is a list of all connected nodes from the current node.
    #Nodes are represented by a node number.
    #Duplicate nodes may not be entered in the list, as paths must be unique.
    def addNode (self, nodeList):
        assert (isinstance (nodeList, list))
        self.nodes.append (nodeList)
        self.numOfNodes+=1
    
    #Returns a list of all possible groups within the graph.    
    def getPossibleGroups (self):
        result = []
        n = 0
        while (n < self.numOfNodes):
            l = self.doBreadthFirstSearch(n)
            l.sort()
            if (not (l in result)):
                result.append (l)
            n += 1
        return result
    
    #Returns a list of all nodes which may be reached from a given starting node.
    def doBreadthFirstSearch (self, startingNode):
        result = [startingNode]
        a = [startingNode]
        while (len(a) > 0):
            n = a.pop(0)
            for l in self.nodes[n]:
                if (not l in result):
                    a.append (l)  
                    result.append (l)
        return result
    
    #Returns the number of nodes in the graph.
    def getNumberOfNodes (self):
        return self.numOfNodes
    
    #Returns the shortest path from a starting node to a finishing node.
    def getShortestPath (self, start, finish):
        self.shortestPath = []
        a = [start]
        self.doPathIteration (start, finish, a)
        return self.shortestPath
    
    def doPathIteration (self, current, finish, array):
        for n in self.nodes[current]:
            if (not (n in array)):
                array.append (n)
                if (not (n == finish)):
                    self.doPathIteration (n, finish, array)
                else:
                    if (len (self.shortestPath) == 0):
                        self.shortestPath = deepcopy(array)
                    if (len (array) < len (self.shortestPath)):
                        self.shortestPath = deepcopy(array)
                    array.pop(len(array) - 1)
                    break
                array.pop(len(array) - 1)
        return
               
    #Returns a string representation of the graph. Each node is displayed on a separate line with a list
    #of connected nodes following a semicolon.
    def toString(self):
        i=0
        for l in self.nodes:
            print (str (i) + ": ", end="")
            i+=1
            j=0
            for node in l:
                    if (j >= len (l) - 1):
                        print (str (node))
                    else:
                        print (str (node) + ", ", end="")
                    j+=1