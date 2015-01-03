from splitviewfuse.filehandlecontainers.FileHandleContainer import FileHandleContainer
from splitviewfuse.virtualfiles.Segment2SingleVirtualFile import Segment2SingleVirtualFile

class Segment2SingleVirtualFileHandleContainer(FileHandleContainer):
    
    def __init__(self, maxSegmentSize):
        super(Segment2SingleVirtualFileHandleContainer, self).__init__()
        self.maxSegmentSize = maxSegmentSize
        
    def _FileHandleContainer__createHandleObject(self, path):
        return Segment2SingleVirtualFile(path, self.maxSegmentSize)
        
    def _FileHandleContainer__cleanupHandleObject(self, handleObject):
        handleObject.closeFileHandle()
