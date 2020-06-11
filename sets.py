from copy import deepcopy

#Returns true if set1 is a subset of set 2.
def isSubset (set1, set2):
    result = False
    if (len (set1) < len (set2)):
        result = True
        s = deepcopy (set2)
        s.sort()
        for n in set1:
            if (not (n in s)):
                result = False
                break
    return result    

#Returns true if the list is a unique set of numbers
def isUniqueSet (l):
    result=True
    c = deepcopy (l)
    while (len(c) > 0):
        n = c.pop(0)
        for m in c:
            if (n == m):
                result=False
                c=[]
                break
    return result