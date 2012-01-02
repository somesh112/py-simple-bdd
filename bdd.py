# Copyright 2011 Craig Eales

# This file is part of py-simple-bdd.

# py-simple-bdd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# py-simple-bdd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with py-simple-bdd.  If not, see <http://www.gnu.org/licenses/>.

class Node(object):

    class __TrueNode:
        def __repr__(self):
            return __name__+".Node.T"

        def __hash__(self):
            return 1;

    class __FalseNode:
        def __repr__(self):
            return __name__+".Node.F"

        def __hash__(self):
            return 0;

    T=__TrueNode()
    F=__FalseNode()

    def __init__(self,variable,trueNode,falseNode):
        self.__hash = (hash(variable)+hash(trueNode)-hash(falseNode)) % 0xFFFFFFFF
        self.__variable = variable
        self.__trueNode = trueNode
        self.__falseNode = falseNode

    @property
    def variable(self):
        return self.__variable

    @property
    def trueNode(self):
        return self.__trueNode

    @property
    def falseNode(self):
        return self.__falseNode

    def __hash__(self):
        return self.__hash

    def __eq__(self,other):
        if isinstance(other,Node):
            return \
                self is other or (
                self.__hash == other.__hash and\
                self.variable == other.variable and\
                self.trueNode == other.trueNode and\
                self.falseNode == other.falseNode )
        else:
            return False

    def __ne__(self,other):
        return not self.__eq__(other)

    def __repr__(self):
        return __name__+".Node(" \
            + repr(self.variable) +"," \
            + repr(self.trueNode) +"," \
            + repr(self.falseNode) + ")"

def countLogicalNodes(aNode):
    """Returns the number of logical (==) nodes in the BDD"""
    def cn(aNode,cache):
        if aNode in cache:
            pass
        else:
            if isinstance(aNode,Node):
                cn(aNode.trueNode,cache)
                cn(aNode.falseNode,cache)
            cache.add(aNode)
    cache=set()
    cn(aNode,cache)
    return len(cache)

def countPhysicalNodes(aNode):
    """Returns the number of physical (id) nodes in the BDD"""
    def cn(aNode,cache):
        if id(aNode) in cache:
            pass
        else:
            if isinstance(aNode,Node):
                cn(aNode.trueNode,cache)
                cn(aNode.falseNode,cache)
            cache.add(id(aNode))
    cache=set()
    cn(aNode,cache)
    return len(cache)

def removeRedundant(aNode):
    """Return a new BDD with redundant nodes removed
    a node is redundant if falseNode == trueNode"""
    def r(aNode,cache):
        if aNode in cache:
            return cache[aNode]
        else:
            result=None
            t=r(aNode.trueNode,cache)
            f=r(aNode.falseNode,cache)
            if ( t == f ):
                result=t
            else:
                if ( id(t) == id(aNode.trueNode) and
                     id(f) == id(aNode.falseNode) ):
                    result=aNode
                else:
                    result=Node(aNode.variable,t,f)
            cache[aNode]=result
            return result
    return r(aNode,dict({ Node.T : Node.T,
                          Node.F : Node.F}))

def restrict(aNode,assignments):
    """Return a new BDD which is logically equivalent to aNode
    with variables restricted to the values in the map assignments"""
    def r(aNode,assignments,cache):
        if aNode in cache:
            return cache[aNode]
        else:
            result=None
            if aNode.variable in assignments:
                if assignments[aNode.variable] or assignments[aNode.variable] == Node.T:
                    result=r(aNode.trueNode,assignments,cache)
                else:
                    result=r(aNode.falseNode,assignments,cache)
            else:
                t=r(aNode.trueNode,assignments,cache)
                f=r(aNode.falseNode,assignments,cache)
                if ( id(t) == id(aNode.trueNode) and
                     id(f) == id(aNode.falseNode) ):
                    result=aNode
                else:
                    result=Node(aNode.variable,t,f)
            cache[aNode]=result
            return result
    return r(aNode,assignments,dict({ Node.T : Node.T,
                                      Node.F : Node.F}))

def evaluate(aNode,variable,value):
    return restrict(aNode,{variable:value})

def makePhysicalFromLogical(aNode):
    return restrict(aNode,{})

def simplify(aNode):
    """simply removeRedundant(makePhysicalFromLogical())"""
    return removeRedundant(makePhysicalFromLogical(aNode))

def isTerminal(aNode):
    """Tests if aNode is Node.T or Node.F"""
    return \
        aNode == Node.T or \
        aNode == Node.F

def getTerminal(value):
    """Returns the terminal corresponding to the boolean interpretation of value"""
    if value:
        return Node.T
    else:
        return Node.F

def negate(aNode):
    """Returns a BDD that is the negation of aNode"""
    def n(aNode,cache):
        if aNode == Node.T:
            return Node.F
        elif aNode == Node.F:
            return Node.T
        elif aNode in cache:
            return cache[aNode]
        else:
            t=n(aNode.trueNode,cache)
            f=n(aNode.falseNode,cache)
            if id(t) == id(aNode.trueNode) and \
                    id(f) == id(aNode.falseNode):
                r=aNode
            else:
                r=Node(aNode.variable,t,f)
            cache[aNode]=r
            return r
    return n(aNode,{})

def variable(v):
    return Node(v,Node.T,Node.F)

def notVariable(v):
    return Node(v,Node.F,Node.T)

def conjunction(variables):
    """Form a bdd that is the true iff all of the variables are true.
    the bdd has the variables in the same order as in the iteration.

    >>> bdd.conjunction(['x','y','z'])
    bdd.Node('x',bdd.Node('y',bdd.Node('z',bdd.Node.T,bdd.Node.F),bdd.Node.F),bdd.Node.F)"""
    def c(i):
        try:
            return Node(next(i),c(i),Node.F)
        except StopIteration:
            return Node.T
    return c(iter(variables))

def disjunction(variables):
    """Form a bdd that is the false iff all of the variables are false.
    the bdd has the variables in the same order as in the iteration.

    >>> bdd.disjunction(['x','y','z'])
    bdd.Node('x',bdd.Node.T,bdd.Node('y',bdd.Node.T,bdd.Node('z',bdd.Node.T,bdd.Node.F)))"""
    def d(i):
        try:
            return Node(next(i),Node.T,d(i))
        except StopIteration:
            return Node.F
    return d(iter(variables))

def andOperation(v1,v2):
    if v1 == Node.T:
        return v2
    else:
        return Node.F

def orOperation(v1,v2):
    if v1 == Node.T:
        return Node.T
    else:
        return v2

def extendOrderingToTerminals(ordering):
    """Extend an ordering between Nodes defined by ordering,
    to include Node.T an Node.F such that,
    Node < Node.T < Node.F"""
    def r(x,y):
        if y is Node.F:
            return True
        elif y is Node.T:
            return not x is Node.F
        elif isTerminal(x):
            return False
        else:
            return ordering(x,y)
    return r

leftistOrdering=extendOrderingToTerminals(lambda x,y: True)
rightistOrdering=extendOrderingToTerminals(lambda x,y: False)

def enumeratedVariablesOrdering(variables):
    resultSet=set()
    l=list(variables)
    for i in range(0,len(l)):
        for j in range(i+1,len(l)):
            resultSet.add((l[i],l[j]))
    def o(n1,n2):
        return (n1.variable,n2.variable) in resultSet
    return extendOrderingToTerminals(o)

def apply(node1,node2,binaryOperation,nodeOrdering = leftistOrdering):
    if isTerminal(node1) and isTerminal(node2):
        return binaryOperation(node1,node2)
    else:
        if nodeOrdering(node1,node2):
            return Node(node1.variable,
                        apply(evaluate(node1.trueNode,node1.variable,True),
                              evaluate(node2,node1.variable,True),
                              binaryOperation),
                        apply(evaluate(node1.falseNode,node1.variable,False),
                              evaluate(node2,node1.variable,False),
                              binaryOperation))
        else:
            return Node(node2.variable,
                        apply(evaluate(node2.trueNode,node2.variable,True),
                              evaluate(node1,node2.variable,True),
                              binaryOperation),
                        apply(evaluate(node2.falseNode,node2.variable,False),
                              evaluate(node1,node2.variable,False),
                              binaryOperation))
