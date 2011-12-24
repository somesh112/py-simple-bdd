
class Node(object):

    class __TrueNode:
        def evaluate(self,variable,value):
            return self

        def __repr__(self):
            return "Node.T"

    class __FalseNode:
        def evaluate(self,variable,value):
            return self

        def __repr__(self):
            return "Node.F"

    T=__TrueNode()
    F=__FalseNode()

    def __init__(self,variable,trueNode,falseNode):
        self.variable = variable
        self.trueNode = trueNode
        self.falseNode = falseNode

    def evaluate(self,variable,value):
        if self.variable == variable:
            if value:
                return self.trueNode
            else:
                return self.falseNode
        else:
            return Node(variable,
                        trueNode.evaluate(variable,value),
                        flaseNode.evaluate(variable,value))

    def __eq__(self,other):
        if isinstance(other,Node):
            return \
                self.variable == other.variable and\
                self.trueNode == other.trueNode and\
                self.falseNode == other.falseNode
        else:
            return False

    def __repr__(self):
        return "Node(" \
            + repr(self.variable) +"," \
            + repr(self.trueNode) +"," \
            + repr(self.falseNode) + ")"



