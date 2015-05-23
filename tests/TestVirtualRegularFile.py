import unittest
from splitviewfuse.virtualfiles.VirtualRegularFile import VirtualRegularFile
import os
from tests.VirtualFileTestBase import VirtualFileTestBase


class TestVirtualRegularFile(VirtualFileTestBase, unittest.TestCase):

    def createTestSubject(self, path, maxSegmentSize):
        return VirtualRegularFile(path, maxSegmentSize)

    def testConstructionWithSegmentedFileWorks(self):
        with VirtualRegularFile(self.tmpDir.segment1File, VirtualFileTestBase.SEGMENT_SIZE):
            pass
        
    def testConstructionWithLastSegmentOfFileWorks(self):
        with VirtualRegularFile(self.tmpDir.segment2File, VirtualFileTestBase.SEGMENT_SIZE):
            pass
        
    def testConstructionWithNotSegmentedFileWorks(self):
        with VirtualRegularFile(self.tmpDir.regularfile2, VirtualFileTestBase.SEGMENT_SIZE):
            pass

    def testConstructionWithTooLargeNotSegmentedFileFails(self):
        with self.assertRaises(ValueError):
            with VirtualRegularFile(self.tmpDir.regularfile, VirtualFileTestBase.SEGMENT_SIZE):
                pass
            
    def testConstructionWithTooLargeSegmentOfFileFails(self):
        with self.assertRaises(ValueError):
            with VirtualRegularFile(self.tmpDir.tooBigSegmentFile, VirtualFileTestBase.SEGMENT_SIZE):
                pass
            
    def testConstructionWithNotContinuousSegmentFileFails(self):
        with self.assertRaises(ValueError):
            with VirtualRegularFile(self.tmpDir.brokenNumberSegmentfile, VirtualFileTestBase.SEGMENT_SIZE):
                pass
            
    def testConstructionWithNotExistingFileFails(self):
        with self.assertRaises(ValueError):
            with VirtualRegularFile(self.tmpDir.notExistingFile, VirtualFileTestBase.SEGMENT_SIZE):
                pass
            
    def testConstructionWithNotExistingFileSegmentFails(self):
        with self.assertRaises(ValueError):
            with VirtualRegularFile(self.tmpDir.notExistingSegmentFile, VirtualFileTestBase.SEGMENT_SIZE):
                pass
            
    def testGetFileSizeOfSegmentedFile(self):
        with VirtualRegularFile(self.tmpDir.segment2File, VirtualFileTestBase.SEGMENT_SIZE) as subject:
            expectedSize = os.path.getsize(self.tmpDir.segment1File) + os.path.getsize(self.tmpDir.segment2File)
            self.assertEqual(expectedSize, subject.size())
            
    def testReadSegmentedFileWorks(self):
        with VirtualRegularFile(self.tmpDir.segment2File, VirtualFileTestBase.SEGMENT_SIZE) as subject:
            # from start to end of first segment
            readOffset = 0
            readSize = os.path.getsize(self.tmpDir.segment1File)
            self.assertEqualRead(subject, readOffset, readSize, self.tmpDir.segment1File, readOffset, readSize)
             
            # from start of second segment to its end
            readOffset = readSize
            readSize = os.path.getsize(self.tmpDir.segment2File)
            self.assertEqualRead(subject, readOffset, readSize, self.tmpDir.segment2File, 0, readSize)
 
            # read more than available
            readOffset = 0
            readSize = os.path.getsize(self.tmpDir.segment1File) + os.path.getsize(self.tmpDir.segment2File) + VirtualFileTestBase.SEGMENT_SIZE
            expectedContent = VirtualFileTestBase.read(self.tmpDir.segment1File, 0, VirtualFileTestBase.SEGMENT_SIZE) + VirtualFileTestBase.read(self.tmpDir.segment2File, 0, VirtualFileTestBase.SEGMENT_SIZE)
            actualContent = subject.read(0, readSize)
            self.assertEqual(expectedContent, actualContent)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()