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
        self.assertEqual(bdd.Node.T.evaluate('a variable',False),bdd.Node.T)
        self.assertEqual(bdd.Node.T.evaluate('a variable',True),bdd.Node.T)

    def testFalse(self):
        self.assertEqual(bdd.Node.F,bdd.Node.F)
        self.assertNotEqual(bdd.Node.F,bdd.Node.T)
        self.assertEqual(bdd.Node.F,eval(repr(bdd.Node.F)))
        self.assertEqual(bdd.Node.F.evaluate('a variable',False),bdd.Node.F)
        self.assertEqual(bdd.Node.F.evaluate('a variable',True),bdd.Node.F)

    def testSingleNode(self):
        n1=bdd.Node('x1',bdd.Node.T,bdd.Node.F)
        self.assertEqual(n1,n1)
        self.assertEqual(n1,eval(repr(n1)))
        self.assertEqual(n1.evaluate('x1',True),bdd.Node.T)
        self.assertEqual(n1.evaluate('x1',False),bdd.Node.F)
        self.assertEqual(n1.evaluate('not x1',True),n1)
        n2=bdd.Node('x2',bdd.Node.T,bdd.Node.F)
        self.assertNotEqual(n1,n2)
        n3=bdd.Node('x1',bdd.Node.T,bdd.Node.T)
        self.assertNotEqual(n1,n3)
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
        self.assertEqual(cn1,eval(repr(cn1)))
        self.assertEqual(cn1.evaluate('x2',True),n1)
        self.assertEqual(cn1.evaluate('x2',False),n2)
        self.assertEqual(cn1.evaluate('x1',True).evaluate('x2',True),bdd.Node.T)
        self.assertEqual(cn1.evaluate('x1',True).evaluate('x2',False),bdd.Node.F)
        self.assertEqual(cn1.evaluate('x1',False).evaluate('x2',True),bdd.Node.F)
        self.assertEqual(cn1.evaluate('x1',False).evaluate('x2',False),bdd.Node.T)
        self.assertEqual(cn1.evaluate('x2',True).evaluate('x1',True),bdd.Node.T)
        self.assertEqual(cn1.evaluate('x2',False).evaluate('x1',True),bdd.Node.F)
        self.assertEqual(cn1.evaluate('x2',True).evaluate('x1',False),bdd.Node.F)
        self.assertEqual(cn1.evaluate('x2',False).evaluate('x1',False),bdd.Node.T)

if __name__ == '__main__':
    unittest.main()
