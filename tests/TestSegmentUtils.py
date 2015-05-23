import unittest
from splitviewfuse.SegmentUtils import SegmentUtils


class TestSegmentUtils(unittest.TestCase):
       
    def testSplitSegmentPath(self):
        segmentedPath = 'a.file.name.seg.1'
        actualFilePath, actualSegmentNumber = SegmentUtils.splitSegmentPath(segmentedPath)
        self.assertEqual('a.file.name', actualFilePath)
        self.assertEqual(1, actualSegmentNumber)

    def testSplitSegmentPathPrefixedWithZero(self):
        segmentedPath = 'a.file.name.seg.02'
        actualFilePath, actualSegmentNumber = SegmentUtils.splitSegmentPath(segmentedPath)
        self.assertEqual('a.file.name', actualFilePath)
        self.assertEqual(2, actualSegmentNumber)
        
    def testDoNotSplitPathIfSeparatorInside(self):
        segmentedPath = 'a.file.name.seg.1.qq'
        actualFilePath, actualSegmentNumber = SegmentUtils.splitSegmentPath(segmentedPath)
        self.assertEqual(segmentedPath, actualFilePath)
        self.assertIsNone(actualSegmentNumber, 'There should not be a segment number.')
        
    def testJoinSegmentedPath(self):
        joinedPath = SegmentUtils.joinSegmentPath('qq.abc.123', 2)
        self.assertEqual('qq.abc.123.seg.2', joinedPath)
        
    def testJoinSegmentedPathWithoutSegmentNumber(self):
        joinedPath = SegmentUtils.joinSegmentPath('abc.123.fsd', None)
        self.assertEqual('abc.123.fsd', joinedPath)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()