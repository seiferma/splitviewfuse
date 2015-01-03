from splitviewfuse.virtualfiles.VirtualFile import VirtualFile, LazyFile
from splitviewfuse.SegmentUtils import SegmentUtils
import os
from errno import ENOENT

class Segment2SingleVirtualFile(VirtualFile):
    
    def __init__(self, absRootPath, maxSegmentSize):
        self.allSegments = self.__findAllSegments(absRootPath)
        self.maxSegmentSize = maxSegmentSize
        if len(self.allSegments) < 1:
            raise OSError(ENOENT)
        super(Segment2SingleVirtualFile, self).__init__(self.allSegments[-1].getPath())
        self.sz = (len(self.allSegments) - 1) * maxSegmentSize + os.path.getsize(self.allSegments[-1].getPath())

    def read(self, offset, size):
        firstSegmentIndex = offset // self.maxSegmentSize
        segmentOffset = offset - (firstSegmentIndex * self.maxSegmentSize)
        
        data = b""
        remainingSize = size
        for segment in self.allSegments[firstSegmentIndex:]:
            readData = segment.read(segmentOffset, remainingSize)
            remainingSize -= len(readData)
            data += readData
            segmentOffset = 0
            if remainingSize <= 0:
                break
        
        return data
    
    def size(self):
        return self.sz
    
    def closeFileHandle(self):
        for segment in self.allSegments:
            segment.close()
            
    def __findAllSegments(self, path):
        absRootPathDir = os.path.dirname(path)
        fileName = os.path.basename(path)
        segmentName, segmentNumber = SegmentUtils.splitSegmentPath(fileName)
        if segmentNumber is None and os.path.exists(path):
            return [LazyFile(path)]
        
        entries = list()
        for entry in os.listdir(absRootPathDir):
            entryBase, _ = SegmentUtils.splitSegmentPath(entry)
            if entryBase == segmentName:
                entries.append(LazyFile(os.path.join(absRootPathDir, entry)))
        entries.sort(key=lambda x: SegmentUtils.splitSegmentPath(x.getPath())[1])
        return entries

        