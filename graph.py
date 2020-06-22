from sets import *
from math import floor
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
    
    def getWeight (self, node):
        return self.weights[node]
    
    def setWeight (self, node, value):
        self.weights[node] = value
    
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
    
    def balanceGraph (self, showSteps):
        groups = self.getPossibleGroups()
        print ("Groups: " + str(groups))
        stepCount = 0
        #Iterate over each group of connected nodes in the graph.
        for group in groups:
            totalWeight = 0
            balancedNodeWeight = 0 
            heaviestNode = 0
            lightestNode = 0
            groupWeights = []
            w = 0
            w2 = _Infinity
            #Find weight information in the group.
            for node in group:
                groupWeights.append (self.weights[node])
                totalWeight += self.weights[node]
                if (self.weights[node] > w):
                    w = self.weights[node]
                    heaviestNode = node
                if (self.weights[node] < w2):
                    w2 = self.weights[node]
                    lightestNode = node
            #Calculate the weight required for each node in order for the group to be balanced. Note that in some cases weights may differ by one.
            balancedNodeWeight = floor(totalWeight / len (group))
            if (not(len(group) * balancedNodeWeight == totalWeight) and balancedNodeWeight == self.weights[lightestNode]):
                balancedNodeWeight += 1
            #Calculate if the group is balanced.
            isBalanced = self.isArrayBalanced (group)
            if (isBalanced == True and showSteps == True):
                print (self.toString())
            #Distribute weights of nodes until the group is balanced.
            while (isBalanced == False):
                if (self.numOfNodes <= 1):
                    break
                paths = []
                #Find weight information in the group.
                for node in group:
                    if (self.weights[node] > self.weights[heaviestNode]):
                        heaviestNode = node
                    if (self.weights[node] < self.weights[lightestNode]):
                        lightestNode = node
                #Calculate the weight required for each node in order for the group to be balanced. Note that in some cases weights may differ by one.
                balancedNodeWeight = floor(totalWeight / len (group))
                if (not(len(group) * balancedNodeWeight == totalWeight) and balancedNodeWeight == self.weights[lightestNode]):
                    balancedNodeWeight += 1
                #Find the shortest paths from the heaviest node to all other nodes in the group.
                for n in group:
                    if (n == heaviestNode):
                        continue
                    else:
                        paths.append (self.getShortestPath(heaviestNode, n))
                #Merge path subsets together.
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
                #Distribute the required amount needed to balance each node in each path.
                for path in paths:
                    if (len(path) < 2):
                        continue
                    distributionAmount = 0
                    firstNode = path.pop(0)
                    #Find the amount needed to balance each node in each path
                    for neighbor in path:
                        a = balancedNodeWeight - self.weights[neighbor]
                        if (a < 0):
                            a = 0
                        distributionAmount += a
                    if (distributionAmount == 0):
                        continue
                    lenNeighbors = len(path)
                    nextNode = path.pop(0)
                    diff = self.weights[firstNode] - distributionAmount
                    if (diff < balancedNodeWeight):
                        distributionAmount = self.weights[firstNode] - balancedNodeWeight
                        diff = balancedNodeWeight
                    #Distribute the amount to the next node in the path.
                    self.weights[firstNode] = int (diff)
                    self.weights[nextNode] = int (self.weights[nextNode] + distributionAmount)
                    if (showSteps == True): 
                        print (self.toString())
                    stepCount+=1
                isBalanced = self.isArrayBalanced (group)
        print (self.toString())
        print ("The graph has been balanced in " + str(stepCount) + " steps.")
        return
    
    #Returns true if the array contains values which differ by no more than one.
    def isArrayBalanced (self, a):
        isBalanced = True
        if (len (a) > 0):
            groupWeights = []
            for node in a:
                groupWeights.append (self.weights[node])
            groupWeights.sort()
            if (abs(groupWeights[0] - groupWeights[len(groupWeights) - 1]) > 1):
                isBalanced = False
        return isBalanced
    
    #Returns true if the graph is balanced.
    def isBalanced (self):
        result = True
        arrays = self.getPossibleGroups()
        for array in arrays:
            if (self.isArrayBalanced (array) == False):
                result = False
                break
        return result
    
    #Return the neighbors of a node
    def getNeighbors (self, node):
        return self.nodes[node]
    
    #sets the value of the neighbor array for a given node.
    def setNeighbors (self, node, neighbors):
        self.nodes[node] = neighbors
               
    #Returns a string representation of the graph. Each node is displayed on a separate line with a list
    #of connected nodes following a semicolon.
    def toString(self):
        i=0
        for l in self.nodes:
            print ("[" + str (i) + ", " + str(self.weights[i]) + "]" + ": ", end="")
            i+=1
            j=0
            if (len (l) == 0):
                print ()
            for node in l:
                    if (j >= len (l) - 1):
                        print ("[" + str(node) + ", " + str(self.weights[node]) + "]")
                    else:
                        print ("[" + str(node) + ", " + str(self.weights[node]) + "]" + ", ", end="")
                    j+=1