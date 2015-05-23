from abc import ABCMeta, abstractmethod
from splitviewfuse.SegmentUtils import SegmentUtils
from tests.TestTmpDirectory import TestTmpDirectory
from math import ceil, floor
import os

class VirtualFileTestBase(object):
    
    __metaclass__ = ABCMeta
    
    SEGMENT_SIZE = 16

    def setUp(self):
        self.tmpDir = TestTmpDirectory(VirtualFileTestBase.SEGMENT_SIZE)
        
    def tearDown(self):
        self.tmpDir.removeDir()
    
    
    def testConstructionWithNoneMaximumSegmentSizeFails(self):
        with self.assertRaises(ValueError):
            with self.createTestSubject(self.tmpDir.regularfile2, None):
                pass
            
    def testConstructionWithZeroMaximumSegmentSizeFails(self):
        with self.assertRaises(ValueError):
            with self.createTestSubject(self.tmpDir.regularfile2, 0):
                pass
            
    def testConstructionWithNegativeMaximumSegmentSizeFails(self):
        with self.assertRaises(ValueError):
            with self.createTestSubject(self.tmpDir.regularfile2, -1):
                pass
            
    def testConstructionWithNonIntegerMaximumSegmentSizeFails(self):
        with self.assertRaises(ValueError):
            with self.createTestSubject(self.tmpDir.regularfile2, 'abc'):
                pass
            
    def testGetFileSizeOfNotSegmentedFileWorks(self):
        with self.createTestSubject(self.tmpDir.regularfile2, VirtualFileTestBase.SEGMENT_SIZE) as subject:
            self.assertEqual(VirtualFileTestBase.SEGMENT_SIZE, subject.size())
            
    def testReadNotSegmentedFileWorks(self):
        with self.createTestSubject(self.tmpDir.regularfile2, VirtualFileTestBase.SEGMENT_SIZE) as subject:
             
            # from start to half
            readOffset = 0
            readSize = int(ceil(VirtualFileTestBase.SEGMENT_SIZE / 2))
            self.assertEqualRead(subject, readOffset, readSize, self.tmpDir.regularfile2, readOffset, readSize)
             
            # from half to end
            readOffset = readSize
            readSize = int(floor(VirtualFileTestBase.SEGMENT_SIZE / 2))
            self.assertEqualRead(subject, readOffset, readSize, self.tmpDir.regularfile2, readOffset, readSize)
 
            # read more than available
            readOffset = 0
            readSize = 2 * os.path.getsize(self.tmpDir.regularfile2)
            self.assertEqualRead(subject, readOffset, readSize, self.tmpDir.regularfile2, readOffset, readSize)
            
            
            
    
    @abstractmethod
    def createTestSubject(self, path, maxSegmentSize):
        '''
        Creates a test subjects and returns it.
        '''
      
    @staticmethod
    def createSegmentName(basePath, segmentNumber):
        return SegmentUtils.joinSegmentPath(basePath, segmentNumber)
        
    def assertEqualRead(self, virtualFile, vfOffset, vfSize, realFilePath, rfoffset, rfSize):
        actualData = virtualFile.read(vfOffset, vfSize)
        expectedData = VirtualFileTestBase.read(realFilePath, rfoffset, rfSize)
        self.assertEqual(expectedData, actualData)
        
    @staticmethod
    def read(filePath, offset, size):
        with open(filePath, 'rb') as f:
            f.seek(offset)
            return f.read(size)
