import unittest
from tests.SplitViewFuseBaseTestBase import SplitViewFuseBaseTestBase
from splitviewfuse.SplitViewFuse import SplitViewFuse
import os
import shutil

class TestSplitViewFuse(SplitViewFuseBaseTestBase, unittest.TestCase):
    
    def createTestSubject(self, root, maxSegmentSize):
        return SplitViewFuse(root, maxSegmentSize, None, None)
    
    def testReadDir(self):
        shutil.copyfile(self.tmpDir.regularfile, os.path.join(self.tmpDir2, 'bigfile'))
        shutil.copyfile(self.tmpDir.regularfile2, os.path.join(self.tmpDir2, 'smallfile'))
        os.makedirs(os.path.join(self.tmpDir2, 'dir'))
        subject = SplitViewFuse(self.tmpDir2, SplitViewFuseBaseTestBase.SEGMENT_SIZE, None, None)
        
        actualDirContent = subject.readdir('/', None)
        self.assertEqual(6, len(actualDirContent))
        self.assertIn('.', actualDirContent)
        self.assertIn('..', actualDirContent)
        self.assertIn('bigfile.seg.0', actualDirContent)
        self.assertIn('bigfile.seg.1', actualDirContent)
        self.assertIn('smallfile', actualDirContent)
        self.assertIn('dir', actualDirContent)

    def testReadDirExactSegmentSize(self):
        shutil.copyfile(self.tmpDir.segment1File, os.path.join(self.tmpDir2, 'a'))
        subject = SplitViewFuse(self.tmpDir2, SplitViewFuseBaseTestBase.SEGMENT_SIZE/2, None, None)

        actualDirContent = subject.readdir('/', None)
        self.assertEqual(4, len(actualDirContent))
        self.assertIn('.', actualDirContent)
        self.assertIn('..', actualDirContent)
        self.assertIn('a.seg.0', actualDirContent)
        self.assertIn('a.seg.1', actualDirContent)

    def testReadDirBrokenSymlink(self):
        bigFileTmp2 = os.path.join(self.tmpDir2, 'bigfile')
        shutil.copyfile(self.tmpDir.regularfile, bigFileTmp2)
        os.symlink(bigFileTmp2, os.path.join(self.tmpDir2, 'symlink'))
        os.remove(bigFileTmp2)
        subject = SplitViewFuse(self.tmpDir2, SplitViewFuseBaseTestBase.SEGMENT_SIZE, None, None)
        
        actualDirContent = subject.readdir('/', None)
        self.assertEqual(3, len(actualDirContent))
        self.assertIn('.', actualDirContent)
        self.assertIn('..', actualDirContent)
        self.assertIn('symlink', actualDirContent)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()