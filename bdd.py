
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

