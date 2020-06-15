from copy import deepcopy
from sets import *
from math import floor, ceil
from _pydecimal import _Infinity

class graph:
    
    nodes=[]
    weights=[]
    numOfNodes=0
    shortestPath=[]
    
    def __init__ (self):
        self.nodes=[]
        self.weights=[]
        self.numOfNodes=0
        self.shortestPath=[]
        return None
    
    #Add a node to the graph. The input is a list of all connected nodes from the current node.
    #Nodes are represented by a node number.
    #Duplicate nodes may not be entered in the list, as paths must be unique.
    def addNode (self, neighborList, weight):
        assert (isinstance (neighborList, list))
        assert (isinstance (weight, int))
        assert (isUniqueSet (neighborList))
        self.nodes.append (neighborList)
        self.weights.append (weight);
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
    
    def balanceGraph (self):
        groups = self.getPossibleGroups()
        stepCount = 0
        for group in groups:
            totalWeight = 0
            balancedNodeWeight = 0 
            heaviestNode = 0
            lightestNode = 0
            groupWeights = []
            w = 0
            w2 = _Infinity
            for node in group:
                groupWeights.append (self.weights[node])
                totalWeight += self.weights[node]
                if (self.weights[node] > w):
                    w = self.weights[node]
                    heaviestNode = node
                if (self.weights[node] < w2):
                    w2 = self.weights[node]
                    lightestNode = node
            balancedNodeWeight = floor(totalWeight / len (group))
            if (not(len(group) * balancedNodeWeight == totalWeight) and balancedNodeWeight == lightestNode):
                balancedNodeWeight += 1
            paths = []
            isBalanced = True
            v = deepcopy(groupWeights)
            v.sort()
            if (abs(v[0] - v[len(v) - 1]) > 1):
                isBalanced = False
            if (isBalanced == True):
                print (self.toString())
            while (isBalanced == False):
                if (self.numOfNodes <= 1):
                    break
                paths = [] 
                for node in group:
                    if (self.weights[node] > self.weights[heaviestNode]):
                        heaviestNode = node
                for n in group:
                    if (n == heaviestNode):
                        continue
                    else:
                        paths.append (self.getShortestPath(heaviestNode, n))
                #print ("paths" + str(paths))
                i=0
                for path in paths:
                    for p in paths:
                        if (p == path):
                            continue
                        else:
                            if (isSubset(path, p)):
                                paths.pop(i)
                                break
                    i+=1
                #print ("paths " + str(paths))
                for path in paths:
                    if (len(path) < 2):
                        continue
                    distributionAmount = 0
                    first = path.pop(0)
                    #print ("weights: " + str(self.weights))
                    for neighbor in path:
                        a = balancedNodeWeight - self.weights[neighbor]
                        if (a < 0):
                            a = 0
                        distributionAmount += a
                    if (distributionAmount == 0):
                        continue
                    lenNeighbors = len(path)
                    next = path.pop(0)
                    #print ("heaviest" + str(heaviestNode) + "bnw: " + str(balancedNodeWeight) + "lenNeighbors " + str (lenNeighbors) + "dist: " + str(distributionAmount))
                    diff = self.weights[first] - distributionAmount
                    if (diff < balancedNodeWeight):
                        distributionAmount = self.weights[first] - balancedNodeWeight
                        diff = balancedNodeWeight
                    #print (str(distributionAmount) + ", " + str(diff))
                    self.weights[first] = int (diff)
                    self.weights[next] = int (self.weights[next] + distributionAmount)
                    print (self.toString())
                    stepCount+=1      
                isBalanced = True
                groupWeights = []
                for node in group:
                    groupWeights.append (self.weights[node])
                #print (str(groupWeights))
                v = deepcopy(groupWeights)
                v.sort()
                if (abs(v[0] - v[len(v) - 1]) > 1):
                    isBalanced = False
        print ("The graph has been balanced in " + str(stepCount) + " steps.")
        return
               
    #Returns a string representation of the graph. Each node is displayed on a separate line with a list
    #of connected nodes following a semicolon.
    def toString(self):
        i=0
        for l in self.nodes:
            print ("[" + str (i) + ", " + str(self.weights[i]) + "]" + ": ", end="")
            i+=1
            j=0
            for node in l:
                    if (j >= len (l) - 1):
                        print ("[" + str(node) + ", " + str(self.weights[node]) + "]")
                    else:
                        print ("[" + str(node) + ", " + str(self.weights[node]) + "]" + ", ", end="")
                    j+=1