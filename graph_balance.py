from graph import *
from random import random

#Returns a randomized graph with a given number of maximum nodes.
def getRandomGraph (minNumNodes, maxNumNodes):
    g = graph ()
    numNodes = randomint(minNumNodes, maxNumNodes)
    currNode = 0
    i = numNodes
    while (i>0):
        weight = randomint(0, numNodes * 2)
        g.addNode ([], weight)
        i -= 1
    while (currNode < numNodes):
        numNeighbors = randomint(0, numNodes - 1)
        neighbors = []
        possible = []
        j = numNodes - 1
        while (j >= 0):
            if (not (j == currNode)):
                possible.append (j)
            j-=1
        i = numNeighbors
        while (i > 0):
            index = randomint (0, len(possible) - 1)
            neighbor = possible.pop(index)
            neighbors.append (neighbor)
            l = g.getNeighbors(neighbor)
            if (not (currNode in l)):
                l.append (currNode)
            g.setNeighbors (neighbor, l)
            i-=1
        l = g.getNeighbors (currNode)
        for node in neighbors:
            if (not(node in l)):
                l.append (node)
        g.setNeighbors (currNode, l)
        currNode += 1
    return g

def randomint (minNumber, modNumber):
    assert (modNumber <= 10000000000000000 and modNumber >= 0 and minNumber >= 0 and minNumber <= modNumber)
    result = 0
    if (modNumber > 0):
        result = minNumber + (int (random() * 10000000000000000) % (modNumber - minNumber))
    return result


    