from splitviewfuse.virtualfiles.VirtualFile import VirtualFile, LazyFile
from splitviewfuse.SegmentUtils import SegmentUtils
import os
from fuse import FuseOSError
from errno import ENOENT

class Single2SegmentVirtualFile(VirtualFile):

    def __init__(self, absRootPath, maxSegmentSize):
        super(Single2SegmentVirtualFile, self).__init__(absRootPath)
        
        path, nr = SegmentUtils.splitSegmentPath(absRootPath)
        if os.path.islink(path):
            path = os.path.realpath(path)
        
        if nr is None and os.path.isfile(absRootPath) and os.path.getsize(absRootPath) > maxSegmentSize:
            raise FuseOSError(ENOENT)
        
        if nr is None:
            nr = 0
            
        self.path = path
        self.offset = nr * maxSegmentSize
        
        realFileSize = os.path.getsize(self.path)
        if realFileSize <= (nr + 1) * maxSegmentSize:
            # last segment
            self.sz = realFileSize % maxSegmentSize
        else:
            self.sz = maxSegmentSize
            
        self.file = LazyFile(self.path)
        
    def closeFileHandle(self):
        self.file.close()
            
    def read(self, offset, size):
        return self.file.read(self.offset + offset, size)
    
    def size(self):
        return self.sz
