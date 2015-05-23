import unittest
from splitviewfuse.virtualfiles.VirtualFileSegment import VirtualFileSegment
from math import ceil, floor
import os
from tests.VirtualFileTestBase import VirtualFileTestBase
from splitviewfuse.SegmentUtils import SegmentUtils


class TestVirtualFileSegment(VirtualFileTestBase, unittest.TestCase):

    def createTestSubject(self, path, maxSegmentSize):
        return VirtualFileSegment(path, maxSegmentSize)

    def testConstructionWithSegmentedFileWorks(self):
        with VirtualFileSegment(VirtualFileTestBase.createSegmentName(self.tmpDir.regularfile, 1), VirtualFileTestBase.SEGMENT_SIZE):
            pass
        
    def testConstructionWithNotSegmentedFileWorks(self):
        with VirtualFileSegment(self.tmpDir.regularfile2, VirtualFileTestBase.SEGMENT_SIZE):
            pass
        
    def testConstructionWithSymlinkFileWorks(self):
        with VirtualFileSegment(VirtualFileTestBase.createSegmentName(self.tmpDir.slRegularFile, 1), VirtualFileTestBase.SEGMENT_SIZE):
            pass
        
    def testConstructionWithFileInSymlinkDirWorks(self):
        with VirtualFileSegment(VirtualFileTestBase.createSegmentName(self.tmpDir.getFilePathInSymlinkedDir(self.tmpDir.regularfile), 1), VirtualFileTestBase.SEGMENT_SIZE):
            pass
        
    def testConstructionWithTooBigNotSegmentedFileFails(self):
        with self.assertRaises(ValueError):
            with VirtualFileSegment(self.tmpDir.regularfile, VirtualFileTestBase.SEGMENT_SIZE):
                pass
            
    def testConstructionWithTooHighSegmentFileFails(self):
        with self.assertRaises(ValueError):
            subject = VirtualFileSegment(VirtualFileTestBase.createSegmentName(self.tmpDir.regularfile, 2), VirtualFileTestBase.SEGMENT_SIZE)
            subject.closeFileHandle()
        
    def testConstructionWithNotExistingFileFails(self):
        with self.assertRaises(ValueError):
            with VirtualFileSegment(self.tmpDir.notExistingFile, VirtualFileTestBase.SEGMENT_SIZE):
                pass
            
    def testGetFileSizeOfInnerSegmentedFileWorks(self):
        with VirtualFileSegment(VirtualFileTestBase.createSegmentName(self.tmpDir.regularfile, 0), VirtualFileTestBase.SEGMENT_SIZE) as subject:
            self.assertEqual(VirtualFileTestBase.SEGMENT_SIZE, subject.size())
            
    def testGetFileSizeLastSegmentedFileWorks(self):
        with VirtualFileSegment(VirtualFileTestBase.createSegmentName(self.tmpDir.regularfile, 1), VirtualFileTestBase.SEGMENT_SIZE) as subject:
            self.assertEqual(VirtualFileTestBase.SEGMENT_SIZE - 1, subject.size())
            
    def testReadInnerSegmentedFileWorks(self):
        with VirtualFileSegment(VirtualFileTestBase.createSegmentName(self.tmpDir.regularfile, 0), VirtualFileTestBase.SEGMENT_SIZE) as subject:
            
            # from start to half
            readOffset = 0
            readSize = int(ceil(VirtualFileTestBase.SEGMENT_SIZE / 2))
            self.assertEqualRead(subject, readOffset, readSize, self.tmpDir.regularfile, readOffset, readSize)
            
            # from half to end
            readOffset = readSize
            readSize = int(floor(VirtualFileTestBase.SEGMENT_SIZE / 2))
            self.assertEqualRead(subject, readOffset, readSize, self.tmpDir.regularfile, readOffset, readSize)

            # read more than available
            readOffset = 0
            readSize = 2 * os.path.getsize(self.tmpDir.regularfile)
            self.assertEqualRead(subject, readOffset, readSize, self.tmpDir.regularfile, readOffset, VirtualFileTestBase.SEGMENT_SIZE)
            
    def testReadLastSegmentedFileWorks(self):
        segmentSize = VirtualFileTestBase.SEGMENT_SIZE - 1
        with VirtualFileSegment(VirtualFileTestBase.createSegmentName(self.tmpDir.regularfile, 1), VirtualFileTestBase.SEGMENT_SIZE) as subject:
            
            # from start to half
            readOffset = 0
            readSize = int(ceil(segmentSize / 2))
            self.assertEqualRead(subject, readOffset, readSize, self.tmpDir.regularfile, VirtualFileTestBase.SEGMENT_SIZE + readOffset, readSize)
            
            # from half to end
            readOffset = readSize
            readSize = int(floor(segmentSize / 2))
            self.assertEqualRead(subject, readOffset, readSize, self.tmpDir.regularfile, VirtualFileTestBase.SEGMENT_SIZE + readOffset, readSize)

            # read more than available
            readOffset = 0
            readSize = 2 * os.path.getsize(self.tmpDir.regularfile)
            self.assertEqualRead(subject, readOffset, readSize, self.tmpDir.regularfile, VirtualFileTestBase.SEGMENT_SIZE + readOffset, segmentSize)

    def testGetPathForSegmentedFileWorks(self):
        with VirtualFileSegment(VirtualFileTestBase.createSegmentName(self.tmpDir.regularfile, 1), VirtualFileTestBase.SEGMENT_SIZE) as subject:
            expectedPath, _ = SegmentUtils.splitSegmentPath(self.tmpDir.regularfile)
            self.assertEquals(expectedPath, subject.getPath())
        
    def testGetPathForNotSegmentedFileWorks(self):
        with VirtualFileSegment(self.tmpDir.regularfile2, VirtualFileTestBase.SEGMENT_SIZE) as subject:
            self.assertEquals(self.tmpDir.regularfile2, subject.getPath())
            
    def testGetPathForSymlinkFileWorks(self):
        with VirtualFileSegment(VirtualFileTestBase.createSegmentName(self.tmpDir.slRegularFile, 1), VirtualFileTestBase.SEGMENT_SIZE) as subject:
            expectedPath, _ = SegmentUtils.splitSegmentPath(os.path.realpath(self.tmpDir.slRegularFile))
            self.assertEquals(expectedPath, subject.getPath())
         
    def testGetPathForFileInSymlinkDirWorks(self):
        with VirtualFileSegment(VirtualFileTestBase.createSegmentName(self.tmpDir.getFilePathInSymlinkedDir(self.tmpDir.regularfile), 1), VirtualFileTestBase.SEGMENT_SIZE) as subject:
            expectedPath, _ = SegmentUtils.splitSegmentPath(os.path.realpath(self.tmpDir.getFilePathInSymlinkedDir(self.tmpDir.regularfile)))
            self.assertEquals(expectedPath, subject.getPath())

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()