import unittest
from tests.SplitViewFuseBaseTestBase import SplitViewFuseBaseTestBase
from splitviewfuse.UnionViewFuse import UnionViewFuse


class TestUnionViewFuse(SplitViewFuseBaseTestBase, unittest.TestCase):
    
    def createTestSubject(self, root, maxSegmentSize):
        return UnionViewFuse(root, maxSegmentSize)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()