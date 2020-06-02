from math import sqrt

class graph:
    
    nodes=[]
    numOfNodes=0
    
    def __init__ (self):
        return
    
    #Add a node to the graph. The input is a list of all connected nodes from the current node
    #Duplicate nodes may not be entered in the list, as paths must be unique.
    def addNode (self, nodeList):
        assert (isinstance (nodeList, list))
        self.nodes.append (nodeList)
        self.numOfNodes+=1
        
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
                if (not l[0] in result):
                    a.append (l[0])  
                    result.append (l[0])
        return result
    
    def doDepthFirstSearch (self, startingNode):
        result = [startingNode]
        a = [startingNode]
        while (len(a) > 0):
            n = a.pop(0)
            l = self.nodes[n]
            if (len(l) == 0 or l[0][0] in result):
                break
            a.append (l[0][0])
            result.append (l[0][0])
        return result
    
    def getNumberOfNodes (self):
        return self.numOfNodes
    
    def toString(self):
        i=0
        for l in self.nodes:
            print (str (i) + ": ", end="")
            i+=1
            j=0
            for node in l:
                    if (j >= len (l) - 1):
                        print (str (node[0]))
                    else:
                        print (str (node[0]) + ", ", end="")
                    j+=1