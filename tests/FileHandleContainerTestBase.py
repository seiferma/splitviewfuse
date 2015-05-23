from abc import ABCMeta, abstractmethod
from _pyio import __metaclass__
import tempfile
from tests.TestTmpDirectory import TestTmpDirectory


class FileHandleContainerTestBase(object):
    
    __metaclass__ = ABCMeta
    
    def setUp(self):
        self.tmpDir = TestTmpDirectory(16)
        self.subject = self.__createTestSubject()
           
    @abstractmethod 
    def __createTestSubject(self):
        '''
        Create the file handle container to test
        '''
        
    @abstractmethod
    def __getFileForRegularTests(self):
        '''
        bla
        '''

    def tearDown(self):
        self.tmpDir.removeDir()
        
    def testRegisterExistingFile(self):
        index = self.subject.registerHandle(self.__getFileForRegularTests())
        self.assertGreaterEqual(index, 0)
        
    def testRegisterNotExistingFile(self):
        with self.assertRaises(ValueError) as _:
            self.subject.registerHandle(tempfile.mktemp())
            
    def testRegisterNone(self):
        with self.assertRaises(ValueError) as _:
            self.subject.registerHandle(None)
            
    def testRegisterExistingFileTwice(self):
        index1 = self.subject.registerHandle(self.__getFileForRegularTests())
        self.assertGreaterEqual(index1, 0)
        index2 = self.subject.registerHandle(self.__getFileForRegularTests())
        self.assertGreaterEqual(index2, 0)
        self.assertNotEqual(index1, index2)
            
    def testGetHandle(self):
        index = self.subject.registerHandle(self.__getFileForRegularTests())
        handleObject = self.subject.getHandle(index)
        self.assertIsNotNone(handleObject, 'Invalid file handle object has been returned.')
        
    def testGetInvalidHandle(self):
        with self.assertRaises(ValueError) as _:
            self.subject.getHandle(42)
            
    def testGetNoneHandle(self):
        with self.assertRaises(ValueError) as _:
            self.subject.getHandle(None)
            
    def testGetTwoHandlesForSameFile(self):
        index1 = self.subject.registerHandle(self.__getFileForRegularTests())
        index2 = self.subject.registerHandle(self.__getFileForRegularTests())
        
        h1 = self.subject.getHandle(index1)
        self.assertIsNotNone(h1)

        h2 = self.subject.getHandle(index2)
        self.assertIsNotNone(h2)
        
        self.assertNotEqual(h1, h2)
    
    def testUnregisterHandle(self):
        index = self.subject.registerHandle(self.__getFileForRegularTests())
        self.subject.unregisterHandle(index)
        
    def testUnregisterNotExistingHandle(self):
        # fail silently
        self.subject.unregisterHandle(42)
    
