import unittest
from tests.SplitViewFuseBaseTestBase import SplitViewFuseBaseTestBase
from splitviewfuse.UnionViewFuse import UnionViewFuse
import shutil
import os

class TestUnionViewFuse(SplitViewFuseBaseTestBase, unittest.TestCase):
    
    def createTestSubject(self, root, maxSegmentSize):
        return UnionViewFuse(root, maxSegmentSize)

    def testReadDir(self):
        shutil.copyfile(self.tmpDir.segment1File, os.path.join(self.tmpDir2, 'a.seg.0'))
        shutil.copyfile(self.tmpDir.segment1File, os.path.join(self.tmpDir2, 'a.seg.1'))
        shutil.copyfile(self.tmpDir.regularfile2, os.path.join(self.tmpDir2, 'b'))
        os.makedirs(os.path.join(self.tmpDir2, 'c'))
        subject = UnionViewFuse(self.tmpDir2, SplitViewFuseBaseTestBase.SEGMENT_SIZE)
         
        actualDirContent = subject.readdir('/', None)
        self.assertEqual(5, len(actualDirContent))
        self.assertIn('.', actualDirContent)
        self.assertIn('..', actualDirContent)
        self.assertIn('a', actualDirContent)
        self.assertIn('b', actualDirContent)
        self.assertIn('c', actualDirContent)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()