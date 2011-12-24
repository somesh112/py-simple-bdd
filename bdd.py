
class Node(object):

    class __TrueNode:
        def evaluate(self,variable,value):
            return self

        def restrict(self,values):
            return self

        def __repr__(self):
            return __name__+".Node.T"

    class __FalseNode:
        def evaluate(self,variable,value):
            return self

        def restrict(self,values):
            return self

        def __repr__(self):
            return __name__+".Node.F"

    T=__TrueNode()
    F=__FalseNode()

    def __init__(self,variable,trueNode,falseNode):
        self.variable = variable
        self.trueNode = trueNode
        self.falseNode = falseNode

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
                self.variable == other.variable and\
                self.trueNode == other.trueNode and\
                self.falseNode == other.falseNode )
        else:
            return False

    def __repr__(self):
        return __name__+".Node(" \
            + repr(self.variable) +"," \
            + repr(self.trueNode) +"," \
            + repr(self.falseNode) + ")"

