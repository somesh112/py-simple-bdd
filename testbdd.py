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

import bdd
import unittest

class TestNode(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def testTrue(self):
        self.assertEqual(bdd.Node.T,bdd.Node.T)
        self.assertNotEqual(bdd.Node.T,bdd.Node.F)
        self.assertEqual(bdd.Node.T,eval(repr(bdd.Node.T)))
        self.assertEqual(bdd.evaluate(bdd.Node.T,'a variable',False),bdd.Node.T)
        self.assertEqual(bdd.evaluate(bdd.Node.T,'a variable',True),bdd.Node.T)
        self.assertTrue(bdd.isTerminal(bdd.Node.T))
        self.assertEqual(bdd.getTerminal(True),bdd.Node.T)
        self.assertEqual(bdd.getTerminal(['x']),bdd.Node.T)
        self.assertEqual(bdd.negate(bdd.Node.T),bdd.Node.F)

    def testFalse(self):
        self.assertEqual(bdd.Node.F,bdd.Node.F)
        self.assertNotEqual(bdd.Node.F,bdd.Node.T)
        self.assertEqual(bdd.Node.F,eval(repr(bdd.Node.F)))
        self.assertEqual(bdd.evaluate(bdd.Node.F,'a variable',False),bdd.Node.F)
        self.assertEqual(bdd.evaluate(bdd.Node.F,'a variable',True),bdd.Node.F)
        self.assertTrue(bdd.isTerminal(bdd.Node.F))
        self.assertEqual(bdd.getTerminal(False),bdd.Node.F)
        self.assertEqual(bdd.getTerminal([]),bdd.Node.F)
        self.assertEqual(bdd.negate(bdd.Node.F),bdd.Node.T)

    def testSingleNode(self):
        n1=bdd.Node('x1',bdd.Node.T,bdd.Node.F)
        self.assertFalse(bdd.isTerminal(n1))
        self.assertEqual(bdd.countPhysicalNodes(n1),3)
        self.assertEqual(bdd.countLogicalNodes(n1),3)
        self.assertEqual(n1,n1)
        self.assertEqual(n1,eval(repr(n1)))
        self.assertEqual(hash(n1),hash(eval(repr(n1))))
        self.assertEqual(bdd.evaluate(n1,'x1',True),bdd.Node.T)
        self.assertEqual(bdd.evaluate(n1,'x1',False),bdd.Node.F)
        self.assertEqual(bdd.evaluate(n1,'not x1',True),n1)
        n2=bdd.Node('x2',bdd.Node.T,bdd.Node.F)
        self.assertNotEqual(n1,n2)
        n3=bdd.Node('x1',bdd.Node.T,bdd.Node.T)
        self.assertNotEqual(n1,n3)
        self.assertEqual(bdd.countPhysicalNodes(n3),2)
        self.assertEqual(bdd.countLogicalNodes(n3),2)
        n4=bdd.Node('x1',bdd.Node.F,bdd.Node.T)
        self.assertNotEqual(n1,n4)
        n5=bdd.Node('x1',bdd.Node.F,bdd.Node.F)
        self.assertNotEqual(n1,n5)

    def testNestedNode(self):
        n1=bdd.Node('x1',bdd.Node.T,bdd.Node.F)
        n2=bdd.Node('x1',bdd.Node.F,bdd.Node.T)
        n3=bdd.Node('x1',bdd.Node.T,bdd.Node.F)
        cn1=bdd.Node('x2',n1,n2)
        cn2=bdd.Node('x2',n2,n1)
        cn3=bdd.Node('x2',n3,n2)
        self.assertEqual(cn1,cn1)
        self.assertNotEqual(cn1,cn2)
        self.assertEqual(cn1,cn3)
        self.assertEqual(bdd.countLogicalNodes(cn1),5)
        self.assertEqual(bdd.countPhysicalNodes(cn1),5)
        self.assertEqual(hash(cn1),hash(cn3))
        self.assertEqual(cn1,eval(repr(cn1)))
        self.assertEqual(bdd.evaluate(cn1,'x2',True),n1)
        self.assertEqual(bdd.evaluate(cn1,'x2',False),n2)
        self.assertEqual(bdd.evaluate(bdd.evaluate(cn1,'x1',True),'x2',True),bdd.Node.T)
        self.assertEqual(bdd.evaluate(bdd.evaluate(cn1,'x1',True),'x2',False),bdd.Node.F)
        self.assertEqual(bdd.evaluate(bdd.evaluate(cn1,'x1',False),'x2',True),bdd.Node.F)
        self.assertEqual(bdd.evaluate(bdd.evaluate(cn1,'x1',False),'x2',False),bdd.Node.T)
        self.assertEqual(bdd.evaluate(bdd.evaluate(cn1,'x2',True),'x1',True),bdd.Node.T)
        self.assertEqual(bdd.evaluate(bdd.evaluate(cn1,'x2',False),'x1',True),bdd.Node.F)
        self.assertEqual(bdd.evaluate(bdd.evaluate(cn1,'x2',True),'x1',False),bdd.Node.F)
        self.assertEqual(bdd.evaluate(bdd.evaluate(cn1,'x2',False),'x1',False),bdd.Node.T)
        self.assertEqual(bdd.restrict(cn1,{'x1' : True, 'x2' : True}), bdd.Node.T)
        self.assertEqual(bdd.restrict(cn1,{'x1' : True, 'x2' : False}), bdd.Node.F)
        self.assertEqual(bdd.restrict(cn1,{'x1' : False, 'x2' : True}), bdd.Node.F)
        self.assertEqual(bdd.restrict(cn1,{'x1' : False, 'x2' : False}), bdd.Node.T)
        self.assertEqual(bdd.restrict(cn1,{'x1' : False, 'x2' : False}), bdd.Node.T)
        cn4=bdd.Node('x1',bdd.Node('x1',bdd.Node.T,bdd.Node.F),bdd.Node('x1',bdd.Node.T,bdd.Node.F))
        self.assertEqual(bdd.evaluate(cn4,'x1',True),bdd.Node.T)
        self.assertEqual(bdd.evaluate(cn4,'x1',False),bdd.Node.F)
        self.assertEqual(bdd.evaluate(bdd.negate(cn4),'x1',True),bdd.Node.F)
        self.assertEqual(bdd.evaluate(bdd.negate(cn4),'x1',False),bdd.Node.T)
        self.assertEqual(bdd.countPhysicalNodes(cn4),5)
        self.assertEqual(bdd.countLogicalNodes(cn4),4)
        self.assertEqual(bdd.countPhysicalNodes(bdd.restrict(cn4,{})),4)
        self.assertEqual(bdd.removeRedundant(cn4),bdd.Node('x1',bdd.Node.T,bdd.Node.F))
        self.assertEqual(bdd.negate(n1),n2)
        self.assertEqual(bdd.negate(n2),n1)
        self.assertEqual(bdd.negate(bdd.negate(cn1)),cn1)
        self.assertNotEqual(bdd.negate(cn1),cn1)

    def __allOrderings(self,ordering):
        self.assertTrue(ordering(bdd.Node.T,bdd.Node.F))
        self.assertFalse(ordering(bdd.Node.F,bdd.Node.T))
        self.assertTrue(ordering(None,bdd.Node.F))
        self.assertTrue(ordering(None,bdd.Node.T))
        self.assertFalse(ordering(bdd.Node.T,None))
        self.assertFalse(ordering(bdd.Node.F,None))

    def testOrderings(self):
        self.__allOrderings(bdd.leftistOrdering)
        self.assertTrue(bdd.leftistOrdering(None,None))
        self.__allOrderings(bdd.rightistOrdering)
        self.assertFalse(bdd.rightistOrdering(None,None))
        v1=bdd.enumeratedVariablesOrdering(['x1','x2','x3','x4'])
        self.__allOrderings(v1)
        self.assertTrue(v1(bdd.variable('x2'),bdd.variable('x4')))
        self.assertFalse(v1(bdd.variable('x3'),bdd.variable('x2')))

if __name__ == '__main__':
    unittest.main()
