from splitviewfuse.filehandlecontainers.FileHandleContainer import FileHandleContainer
from splitviewfuse.virtualfiles.Single2SegmentVirtualFile import Single2SegmentVirtualFile

class Single2SegmentVirtualFileHandleContainer(FileHandleContainer):
    
    def __init__(self, maxSegmentSize):
        super(Single2SegmentVirtualFileHandleContainer, self).__init__()
        self.maxSegmentSize = maxSegmentSize
        
    def _FileHandleContainer__createHandleObject(self, path):
        return Single2SegmentVirtualFile(path, self.maxSegmentSize)
        
    def _FileHandleContainer__cleanupHandleObject(self, handleObject):
        handleObject.closeFileHandle()
