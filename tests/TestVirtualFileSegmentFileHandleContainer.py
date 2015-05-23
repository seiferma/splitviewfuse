import unittest
from tests.FileHandleContainerTestBase import FileHandleContainerTestBase
from splitviewfuse.filehandlecontainers.VirtualFileSegmentFileHandleContainer import VirtualFileSegmentFileHandleContainer


class TestVirtualFileSegmentFileHandleContainer(FileHandleContainerTestBase, unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestVirtualFileSegmentFileHandleContainer, self).__init__(*args, **kwargs)

    def _FileHandleContainerTestBase__createTestSubject(self):
        return VirtualFileSegmentFileHandleContainer(16)
    
    def _FileHandleContainerTestBase__getFileForRegularTests(self):
        return self.tmpDir.regularfile2


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()