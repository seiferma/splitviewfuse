from abc import ABCMeta, abstractmethod
from _pyio import __metaclass__
from tests.TestTmpDirectory import TestTmpDirectory
from fuse import FuseOSError
import os
import stat
import logging
from tempfile import mkdtemp
import shutil
from splitviewfuse import SplitViewFuseBase
from splitviewfuse.SplitViewFuseBase import ArgumentParserError



class SplitViewFuseBaseTestBase(object):

    __metaclass__ = ABCMeta

    SEGMENT_SIZE = 16
    
    def setUp(self):
        self.tmpDir = TestTmpDirectory(SplitViewFuseBaseTestBase.SEGMENT_SIZE)
        self.subject = self.createTestSubject(self.tmpDir.tmpDir, SplitViewFuseBaseTestBase.SEGMENT_SIZE)
        self.tmpDir2 = mkdtemp()
           
    def tearDown(self):
        self.tmpDir.removeDir()
        shutil.rmtree(self.tmpDir2)

    @abstractmethod
    def createTestSubject(self, root, maxSegmentSize):
        '''
        Creates a test subject and returns it.
        '''
        
    def getRootRelativePath(self, absPath):
        return absPath.replace(self.tmpDir.tmpDir, '')
        
    def testFailOnChmod(self):
        with self.assertRaises(FuseOSError):
            self.subject.chmod(None, None)
            
    def testFailOnChown(self):
        with self.assertRaises(FuseOSError):
            self.subject.chown(None, None, None)
            
    def testFailOnCreate(self):
        with self.assertRaises(FuseOSError):
            self.subject.create(None, None)
            
    def testFailOnLink(self):
        with self.assertRaises(FuseOSError):
            self.subject.link(None, None)
            
    def testFailOnMknod(self):
        with self.assertRaises(FuseOSError):
            self.subject.mknod(None, None, None)
            
    def testFailOnMkdir(self):
        with self.assertRaises(FuseOSError):
            self.subject.mkdir(None, None)
            
    def testFailOnReadlink(self):
        with self.assertRaises(FuseOSError):
            self.subject.readlink(None)
            
    def testFailOnRename(self):
        with self.assertRaises(FuseOSError):
            self.subject.rename(None, None)
            
    def testFailOnRmdir(self):
        with self.assertRaises(FuseOSError):
            self.subject.rmdir(None)
            
    def testFailOnSymlink(self):
        with self.assertRaises(FuseOSError):
            self.subject.symlink(None, None)
            
    def testFailOnTruncate(self):
        with self.assertRaises(FuseOSError):
            self.subject.truncate(None, None)

    def testFailOnUnlink(self):
        with self.assertRaises(FuseOSError):
            self.subject.unlink(None)

    def testFailOnUtimens(self):
        with self.assertRaises(FuseOSError):
            self.subject.utimens(None)
            
    def testFailOnWrite(self):
        with self.assertRaises(FuseOSError):
            self.subject.write(None, None, None, None)

    def testDoNothingOnFlush(self):
        self.subject.flush(None, None)
        
    def testDoNothingOnFsync(self):
        self.subject.fsync(None, None, None)
        
    def testAccessFailsOnWrite(self):
        with self.assertRaises(FuseOSError):
            self.subject.access(self.getRootRelativePath(self.tmpDir.regularfile2), os.W_OK | os.R_OK)
            
    def testAccessSucceedsOnFileRead(self):
        self.subject.access(self.getRootRelativePath(self.tmpDir.regularfile2), os.R_OK)
        
    def testAccessSucceedsOnDirRead(self):
        self.subject.access(self.getRootRelativePath(self.tmpDir.tmpDir), os.R_OK)
        
    def testAccessFailsOnNotAccessibleFile(self):
        with self.assertRaises(FuseOSError):
            self.subject.access(self.getRootRelativePath(self.tmpDir.notAccessibleFile), os.R_OK)
            
    def testGetAttrSucceedsOnDirectory(self):
        actualStats = self.subject.getattr(self.getRootRelativePath(self.tmpDir.tmpDir))
        expectedStats = dict((key, getattr(os.lstat(self.tmpDir.tmpDir), key)) for key in ('st_atime', 'st_ctime',
                'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        expectedStats['st_mode'] = expectedStats['st_mode'] & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH) 
        self.assertDictEqual(expectedStats, actualStats)
        
    def testGetAttrSucceedsOnFile(self):
        actualStats = self.subject.getattr(self.getRootRelativePath(self.tmpDir.regularfile2))
        expectedStats = dict((key, getattr(os.lstat(self.tmpDir.regularfile2), key)) for key in ('st_atime', 'st_ctime',
                'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        expectedStats['st_mode'] = expectedStats['st_mode'] & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH) 
        self.assertDictEqual(expectedStats, actualStats)
        
    def testGetAttrFailsOnMissingFile(self):
        with self.assertRaises(FuseOSError):
            self.subject.getattr(self.getRootRelativePath(self.tmpDir.notExistingFile))
        
    def testGetAttrSucceedsOnSymlinkedFile(self):
        actualStats = self.subject.getattr(self.getRootRelativePath(self.tmpDir.slRegularFile2))
        expectedStats = dict((key, getattr(os.lstat(os.path.realpath(self.tmpDir.slRegularFile2)), key)) for key in ('st_atime', 'st_ctime',
                'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        expectedStats['st_mode'] = expectedStats['st_mode'] & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH) 
        self.assertDictEqual(expectedStats, actualStats)
        
    def testOpenSucceedsOnFile(self):
        fileHandle = self.subject.open(self.getRootRelativePath(self.tmpDir.regularfile2), os.O_RDONLY)
        self.subject.release(None, fileHandle)
        
    def testOpenFailsOnMissingFile(self):
        with self.assertRaises(FuseOSError):
            self.subject.open(self.getRootRelativePath(self.tmpDir.notExistingFile), os.O_RDONLY)
        
    def testOpenFailsOnWriteModes(self):
        writeModes = [os.O_CREAT, os.O_APPEND, os.O_RDWR, os.O_WRONLY ]
        with self.assertRaises(FuseOSError):
            for writeMode in writeModes:
                self.subject.open(self.getRootRelativePath(self.tmpDir.regularfile2), writeMode)
            self.subject.open(self.getRootRelativePath(self.tmpDir.regularfile2), os.O_RDONLY | writeModes[0])
            
    def testReadSucceedsOnFile(self):
        fileHandle = self.subject.open(self.getRootRelativePath(self.tmpDir.regularfile2), os.O_RDONLY)
        actualRead = self.subject.read(None, 1, 0, fileHandle)
        self.subject.release(None, fileHandle)
        
        with open(self.tmpDir.regularfile2, 'r') as f:
            self.assertEqual(f.read(1), actualRead)
            
    def testReadFailsOnUnknownFileHandle(self):
        with self.assertRaises(FuseOSError):
            self.subject.read(None, 1, 0, None)
            
    def testArgumentParsingSucceedsOnMinimalCommand(self):
        arguments = [None, '-o', 'segmentsize=12', self.tmpDir.tmpDir, self.tmpDir2]
        parsedArguments = SplitViewFuseBase.parseArguments(arguments)
        self.__assertArguments(self.tmpDir.tmpDir, self.tmpDir2, 12, None, None, parsedArguments)
        self.assertEqual(0, len(parsedArguments.mountOptions['other']))
        
    def testArgumentParsingSucceedsWithAdditionalOptions(self):
        arguments = [None, '-o', 'segmentsize=12,allow_others,foreground,abc=123,loglevel=info,logfile=/tmp/123.log', self.tmpDir.tmpDir, self.tmpDir2]
        parsedArguments = SplitViewFuseBase.parseArguments(arguments)
        self.__assertArguments(self.tmpDir.tmpDir, self.tmpDir2, 12, logging.INFO, "/tmp/123.log", parsedArguments)
        self.assertEqual(3, len(parsedArguments.mountOptions['other']))
        self.assertTrue(parsedArguments.mountOptions['other']['allow_others'])
        self.assertTrue(parsedArguments.mountOptions['other']['foreground'])
        self.assertEqual('123', parsedArguments.mountOptions['other']['abc'])
        
    def __assertArguments(self, device, mountPoint, segmentSize, loglevel, logfile, parsedArguments):
        self.assertEqual(device, parsedArguments.device)
        self.assertEqual(mountPoint, parsedArguments.dir)
        self.assertEqual(4, len(parsedArguments.mountOptions))
        self.assertEqual(segmentSize, parsedArguments.mountOptions['segmentsize'])
        self.assertEqual(loglevel, parsedArguments.mountOptions['loglevel'])
        self.assertEqual(logfile, parsedArguments.mountOptions['logfile'])
        
    def testArgumentParsingFailsOnNonExistingDevice(self):
        with self.assertRaises(ArgumentParserError):
            arguments = [None, '-o', 'segmentsize=12', self.tmpDir.notExistingFile, self.tmpDir2]
            SplitViewFuseBase.parseArguments(arguments)
        
    def testArgumentParsingFailsOnNonExistingMountPoint(self):
        with self.assertRaises(ArgumentParserError):
            arguments = [None, '-o', 'segmentsize=12', self.tmpDir.tmpDir, self.tmpDir.notExistingFile]
            SplitViewFuseBase.parseArguments(arguments)
            
    def testArgumentParsingFailsOnNonExistingSegmentSize(self):
        with self.assertRaises(ArgumentParserError):
            arguments = [None, '-o', 'abc=123', self.tmpDir.tmpDir, self.tmpDir.notExistingFile]
            SplitViewFuseBase.parseArguments(arguments)
            
    def testArgumentParsingFailsOnInvalidSegmentSize(self):
        with self.assertRaises(ArgumentParserError):
            arguments = [None, '-o', 'segmentsize=a', self.tmpDir.tmpDir, self.tmpDir.notExistingFile]
            SplitViewFuseBase.parseArguments(arguments)
            
    def testArgumentParsingFailsOnZeroSegmentSize(self):
        with self.assertRaises(ArgumentParserError):
            arguments = [None, '-o', 'segmentsize=0', self.tmpDir.tmpDir, self.tmpDir.notExistingFile]
            SplitViewFuseBase.parseArguments(arguments)
    
    def testArgumentParsingFailsOnMissingLogLevelValue(self):
        with self.assertRaises(ArgumentParserError):
            arguments = [None, '-o', 'segmentsize=12,loglevel', self.tmpDir.tmpDir, self.tmpDir2]
            SplitViewFuseBase.parseArguments(arguments)
    
    def testArgumentParsingFailsOnInvalidLogLevel(self):
        with self.assertRaises(ArgumentParserError):
            arguments = [None, '-o', 'segmentsize=12,loglevel=infoa', self.tmpDir.tmpDir, self.tmpDir2]
            SplitViewFuseBase.parseArguments(arguments)
            
    def testArgumentParsingFailsOnMissingLogFileValue(self):
        with self.assertRaises(ArgumentParserError):
            arguments = [None, '-o', 'segmentsize=12,logfile', self.tmpDir.tmpDir, self.tmpDir2]
            SplitViewFuseBase.parseArguments(arguments)
            
    