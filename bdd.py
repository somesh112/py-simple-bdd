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
        def evaluate(self,variable,value):
            return self

        def restrict(self,values):
            return self

        def __repr__(self):
            return __name__+".Node.T"

        def __hash__(self):
            return 1;

    class __FalseNode:
        def evaluate(self,variable,value):
            return self

        def restrict(self,values):
            return self

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

    def evaluate(self,variable,value):
        return self.restrict({ variable : value})

    def restrict(self,values):
        if self.variable in values:
            if values[self.variable]:
                return self.trueNode.restrict(values)
            else:
                return self.falseNode.restrict(values)
        else:
            return Node(self.variable,
                        self.trueNode.restrict(values),
                        self.falseNode.restrict(values))

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

