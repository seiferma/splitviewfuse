from abc import ABCMeta, abstractmethod
from threading import Lock

class FileHandleContainer(object):
    
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self.handles = dict()
        self.freeIndices = list()
        self.lock = Lock()
    
    def registerHandle(self, path):
        if path is None:
            raise ValueError("A path has to be given for registering a handle.")
        with self.lock:
            fileHandleObject = self.createHandleObject(path)
            fileHandleIndex = self.__getNextFreeIndex()
            self.handles[fileHandleIndex] = fileHandleObject
            return fileHandleIndex
    
    def getHandle(self, index):
        with self.lock:
            if not self.handles.has_key(index):
                raise ValueError("Invalid handle indentifier given.")
            return self.handles[index]
    
    def unregisterHandle(self, index):
        with self.lock:
            if index not in self.handles.keys():
                return
            self.freeIndices.append(index)
            handleObject = self.handles.pop(index)
            self.__cleanupHandleObject(handleObject)
        
    def __getNextFreeIndex(self):
        if len(self.freeIndices) > 0:
            return self.freeIndices.pop()
        return len(self.handles)
        
    def createHandleObject(self, path):
        return self.__createHandleObject(path)
        
    @abstractmethod
    def __createHandleObject(self, path):
        '''
        Creates the file handle object for the given path.
        '''
        
    @abstractmethod
    def __cleanupHandleObject(self, handleObject):
        '''
        Cleans up the given handle object.
        '''
