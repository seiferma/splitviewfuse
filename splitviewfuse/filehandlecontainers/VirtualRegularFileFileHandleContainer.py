from splitviewfuse.filehandlecontainers.FileHandleContainer import FileHandleContainer
from splitviewfuse.virtualfiles.VirtualRegularFile import VirtualRegularFile

class VirtualRegularFileFileHandleContainer(FileHandleContainer):
    
    def __init__(self, maxSegmentSize):
        super(VirtualRegularFileFileHandleContainer, self).__init__()
        self.maxSegmentSize = maxSegmentSize
        
    def _FileHandleContainer__createHandleObject(self, path):
        return VirtualRegularFile(path, self.maxSegmentSize)
        
    def _FileHandleContainer__cleanupHandleObject(self, handleObject):
        handleObject.closeFileHandle()
