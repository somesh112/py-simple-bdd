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
                if assignments[aNode.variable]:
                    result=r(aNode.trueNode,assignments,cache)
                else:
                    result=r(aNode.falseNode,assignments,cache)
            else:
                result=Node(aNode.variable,
                            r(aNode.trueNode,assignments,cache),
                            r(aNode.falseNode,assignments,cache))
            cache[aNode]=result
            return result
    return r(aNode,assignments,dict({ Node.T : Node.T,
                                      Node.F : Node.F}))

def evaluate(aNode,variable,value):
    return restrict(aNode,{variable:value})

def makePhysicalFromLogical(aNode):
    return restrict(aNode,{})
