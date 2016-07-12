from splitviewfuse.virtualfiles.VirtualFile import VirtualFile, LazyFile
from splitviewfuse.SegmentUtils import SegmentUtils
import os

class VirtualRegularFile(VirtualFile):
    
    def __init__(self, absRootPath, maxSegmentSize):
        # Validate and save maximum segment size
        if not isinstance(maxSegmentSize, (int, long)) or maxSegmentSize < 1:
            raise ValueError('The maximum segment size must be a positive non-null integer.')
        self.maxSegmentSize = maxSegmentSize
        
        # Look for corresponding segments
        self.allSegments = VirtualRegularFile.__findAllSegments(absRootPath, maxSegmentSize)

        super(VirtualRegularFile, self).__init__(self.allSegments[-1].getPath())
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
            
    @staticmethod
    def __findAllSegments(path, maxSegmentSize):
        #TODO Handle symlinks correctly
        
        # Split the given path
        absRootPathDir = os.path.dirname(path)
        fileName = os.path.basename(path)
        segmentName, segmentNumber = SegmentUtils.splitSegmentPath(fileName)
        
        # If path is not segmented, return the file wrapper for the given path
        if segmentNumber is None and os.path.exists(path):
            if os.path.getsize(path) > maxSegmentSize:
                raise ValueError('Files must not be bigger than the maximum segment size.')
            return [LazyFile(path)]
        
        # If path does not exist, raise error
        if not os.path.exists(absRootPathDir):
            raise ValueError('The directory of the given path {0} does not exist.'.format(path))
        
        # Find all segments belonging to the given path
        entries = list()
        for entry in os.listdir(absRootPathDir):
            entryBase, _ = SegmentUtils.splitSegmentPath(entry)
            if entryBase == segmentName:
                entries.append(LazyFile(os.path.join(absRootPathDir, entry)))
        entries.sort(key=lambda x: SegmentUtils.splitSegmentPath(x.getPath())[1])
        
        if len(entries) < 1:
            raise ValueError('No corresponding segments could be found.')
        
        # Validate found segment numbers
        segmentNumbers = [SegmentUtils.splitSegmentPath(entry.getPath())[1] for entry in entries]
        if not all(i in segmentNumbers for i in range(0, max(segmentNumbers))):
            raise ValueError('Not all required (inner) segments could be found.')
        
        # Validate found segment sizes
        if not all(os.path.getsize(entry.getPath()) == maxSegmentSize for entry in entries[0:-1]) or os.path.getsize(entries[-1].getPath()) > maxSegmentSize:
            raise ValueError('The size of at least one found segment is wrong.')
        
        return entries

        