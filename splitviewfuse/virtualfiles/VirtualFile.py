from abc import ABCMeta, abstractmethod
from threading import Lock
from _pyio import __metaclass__

class VirtualFile(object):
    
    __metaclass__ = ABCMeta
    
    def __init__(self, absRootPath):
        self.path = absRootPath
        
    def __enter__(self):
        return self 

    def __exit__(self, *exc):
        self.closeFileHandle()
        
    def getPath(self):
        return self.path

    @abstractmethod
    def read(self, offset, size):
        '''
        Returns the read bytes from offset with the given size
        or less if EOF is reached.
        '''
    
    @abstractmethod
    def size(self):
        '''
        Returns the size of the file
        '''
    
    @abstractmethod
    def closeFileHandle(self):
        '''
        Closes possibly open file handles
        '''

class LazyFile(object):
    '''
    Wrapper for a file handle object.
    
    The wrapper uses lazy instantiation, so the file handle is not initialized
    before the first usage.
    The wrapper is thread-safe, so it can be used from within multiple threads.
    In such cases the requests to the wrapper are executed sequentially.
    '''
    
    def __init__(self, absPath):
        self.path = absPath
        self.file = None
        self.lock = Lock()
        
    def getPath(self):
        return self.path
        
    def read(self, offset, length):
        with self.lock:
            f = self.__getFile()
            f.seek(offset)
            return f.read(length)
    
    def close(self):
        with self.lock:
            if self.file is not None:
                self.file.close()
                
    def __getFile(self):
        if self.file is None:
            self.file = open(self.path, "rb")
        return self.file
