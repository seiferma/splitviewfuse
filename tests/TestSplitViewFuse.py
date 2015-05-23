import unittest
from tests.SplitViewFuseBaseTestBase import SplitViewFuseBaseTestBase
from splitviewfuse.SplitViewFuse import SplitViewFuse


class TestSplitViewFuse(SplitViewFuseBaseTestBase, unittest.TestCase):
    
    def createTestSubject(self, root, maxSegmentSize):
        return SplitViewFuse(root, maxSegmentSize)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()