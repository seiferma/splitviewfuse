from fuse import FUSE
from splitviewfuse import SplitViewFuseBase
from splitviewfuse.filehandlecontainers.Single2SegmentVirtualFileHandleContainer import Single2SegmentVirtualFileHandleContainer
from splitviewfuse.SegmentUtils import SegmentUtils
import os


class SplitViewFuse(SplitViewFuseBase.SplitViewFuseBase):
    
    def __init__(self, root, maxSegmentSize):
        super(SplitViewFuse, self).__init__(root, maxSegmentSize, Single2SegmentVirtualFileHandleContainer(maxSegmentSize))

    def _SplitViewFuseBase__processReadDirEntry(self, absRootPath, entry):
        dirContent = list()
        
        absRootPathEntry = os.path.join(absRootPath, entry)
        
        # split large files
        if os.path.isfile(absRootPathEntry):
            fileSize = os.path.getsize(absRootPathEntry)
            if fileSize > self.maxFileSize:
                numberOfParts = fileSize // self.maxFileSize + 1
                for i in range(0, numberOfParts):
                    dirContent.append(SegmentUtils.joinSegmentPath(entry, i))
                return dirContent
        
        # return not splitted entry
        dirContent.append(entry)
        return dirContent



def main():
    args = SplitViewFuseBase.parseArguments()
    _ = FUSE(SplitViewFuse(args.device, args.mountOptions['segmentsize']), args.dir, **args.mountOptions['other'])
    #fuse = FUSE(SplitViewFuse(args.device, args.mountOptions['segmentsize']), args.dir, nothreads=True, foreground=True)

if __name__ == '__main__':
    main()
