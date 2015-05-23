from splitviewfuse.virtualfiles.VirtualFile import VirtualFile, LazyFile
from splitviewfuse.SegmentUtils import SegmentUtils
import os
from fuse import FuseOSError
from errno import ENOENT

class VirtualFileSegment(VirtualFile):
    '''
    Virtual file representing a segment of a really existing single file.
    The resulting file starts at some offset with respect to the real file and ends before
    or at the end of the real file. Reading this virtual file means reading a part of the
    real file.
    '''

    def __init__(self, absRootPath, maxSegmentSize):
        '''
        absRootPath is the possibly segmented absolute file path. If the given path is not
        segmented, the file size has to be greater or equal the maxSegmentSize.
        '''
        
        # Validate the given maximum segment size
        if not isinstance(maxSegmentSize, ( int, long )) or maxSegmentSize < 1:
            raise ValueError("The maximum segment size has to be a positive non-null integer.")
        
        # Determine the path of the not segmented file and the segment number
        path, nr = SegmentUtils.splitSegmentPath(absRootPath)
        
        # Resolve symlinks
        path = os.path.realpath(path)
        
        # Abort on non existing path
        if not os.path.exists(path):
            raise ValueError("The given file {0} does not exist.".format(path))
        
        # Ensure that the given file is a segment or is not bigger than the maximum segment size
        if nr is None and os.path.isfile(absRootPath) and os.path.getsize(absRootPath) > maxSegmentSize:
            raise ValueError("The given path refers to a not segmented file that is bigger than the maximum segment size.")
        
        # Fix calculations for not segmented file
        if nr is None:
            nr = 0
            
        # Initialize attributes
        self.realFilePath = path
        self.realFileReadingOffset = nr * maxSegmentSize
        
        
        super(VirtualFileSegment, self).__init__(path)

        # Determine the size of the virtual segment
        realFileSize = os.path.getsize(self.realFilePath)
        if ((nr + 1) * maxSegmentSize) - realFileSize >= maxSegmentSize:
            raise ValueError("The segment number of the given file refers to a not existing part of the underlying file.")
        elif realFileSize < (nr + 1) * maxSegmentSize:
            # last segment that is smaller than maxSegmentSize
            self.sz = realFileSize % maxSegmentSize
        else:
            # all segments before the last one
            self.sz = maxSegmentSize
        
        # Initialize the file handle
        self.file = LazyFile(self.realFilePath)
        
    def closeFileHandle(self):
        self.file.close()
            
    def read(self, offset, size):
        # ensure not reading beyond the borders of the virtual segment
        readSize = min(self.sz - offset, size)
        
        # read the requested content
        return self.file.read(self.realFileReadingOffset + offset, readSize)
    
    def size(self):
        return self.sz
