import os, shutil
from tempfile import mkdtemp, mktemp
import stat

class TestTmpDirectory(object):
    '''
    Test helper for construction of temporary directory holding test files.
    The following files are available:
    - segment1File    (first segment of a file, size is segmentSize)
    - segment2File    (last segment of a file, size is segmentSize - 1
    - regularfile     (file with dummy content, size is 2 * segmentSize - 1)
    - regularfile2    (file with dummy content, size is segmentSize)
    - notExistingFile (file path not pointing to a file)
    '''

    def __init__(self, segmentSize):
        self.__createDir(segmentSize);

    def __createDir(self, segmentSize):
        self.tmpDir = mkdtemp()
        self.segment1File = self.__createFileWithRandomContent(self.tmpDir, 'abc.seg.1', segmentSize)
        self.segment2File = self.__createFileWithRandomContent(self.tmpDir, 'abc.seg.2', segmentSize - 1)
        self.regularfile = self.__createFileWithRandomContent(self.tmpDir, 'def', 2 * segmentSize - 1)
        self.regularfile2 = self.__createFileWithRandomContent(self.tmpDir, 'ghi', segmentSize)
        self.slRegularFile = self.regularfile + '.symlink'
        os.symlink(self.regularfile, self.slRegularFile)
        self.slRegularFile2 = self.regularfile2 + '.symlink'
        os.symlink(self.regularfile2, self.slRegularFile2)
        self.slTmpDir = os.path.join(self.tmpDir, 'tmpDir.symlink')
        os.symlink(self.tmpDir, self.slTmpDir)
        self.notExistingFile = mktemp()
        self.tooBigSegmentFile = self.__createFileWithRandomContent(self.tmpDir, 'jkl.seg.1', segmentSize + 1)
        self.brokenNumberSegmentfile = self.__createFileWithRandomContent(self.tmpDir, 'mno.seg.2', segmentSize)
        self.notExistingSegmentFile = os.path.join(self.tmpDir, 'notExistingSegmentFile.seg.1')
        self.notAccessibleFile = self.__createFileWithRandomContent(self.tmpDir, 'notReadableFile', segmentSize)
        os.chmod(self.notAccessibleFile, os.stat(self.notAccessibleFile).st_mode & ~(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH))
        
    def getFilePathInSymlinkedDir(self, filePath):
        requestedFile = filePath.replace(self.tmpDir, '')
        if requestedFile[0] is os.path.sep:
            requestedFile = requestedFile[1:]
        return os.path.join(self.slTmpDir, requestedFile)    
        
    def removeDir(self):
        shutil.rmtree(self.tmpDir)
        
    @staticmethod
    def __createFileWithRandomContent(dirPath, name, size):
        filePath = os.path.join(dirPath, name)
        with open(filePath, 'wb') as f:
            f.write(os.urandom(size))
        return filePath
