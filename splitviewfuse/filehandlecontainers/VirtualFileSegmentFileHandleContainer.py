from splitviewfuse.filehandlecontainers.FileHandleContainer import FileHandleContainer
from splitviewfuse.virtualfiles.VirtualFileSegment import VirtualFileSegment

class VirtualFileSegmentFileHandleContainer(FileHandleContainer):
    
    def __init__(self, maxSegmentSize):
        super(VirtualFileSegmentFileHandleContainer, self).__init__()
        self.maxSegmentSize = maxSegmentSize
        
    def _FileHandleContainer__createHandleObject(self, path):
        return VirtualFileSegment(path, self.maxSegmentSize)
        
    def _FileHandleContainer__cleanupHandleObject(self, handleObject):
        handleObject.closeFileHandle()
