from fuse import FUSE
from splitviewfuse import SplitViewFuseBase
from splitviewfuse.filehandlecontainers.VirtualFileSegmentFileHandleContainer import VirtualFileSegmentFileHandleContainer
from splitviewfuse.SegmentUtils import SegmentUtils
import os
import sys
from splitviewfuse.SplitViewFuseBase import ArgumentParserError
from argparse import ArgumentTypeError


class SplitViewFuse(SplitViewFuseBase.SplitViewFuseBase):
    
    def __init__(self, root, maxSegmentSize):
        super(SplitViewFuse, self).__init__(root, maxSegmentSize, VirtualFileSegmentFileHandleContainer(maxSegmentSize))

    def _SplitViewFuseBase__processReadDirEntry(self, absRootPath, entry):
        dirContent = list()

        absRootPathEntry = os.path.join(absRootPath, entry)

        # split large files
        if not os.path.isdir(absRootPathEntry):
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
    try:
        args = SplitViewFuseBase.parseArguments(sys.argv)
        _ = FUSE(SplitViewFuse(args.device, args.mountOptions['segmentsize']), args.dir, **args.mountOptions['other'])
        #fuse = FUSE(SplitViewFuse(args.device, args.mountOptions['segmentsize']), args.dir, nothreads=True, foreground=True)
    except ArgumentParserError as e:
        print('Error during command line parsing: {0}'.format(str(e)))
        sys.exit(1)
    except ArgumentTypeError as e:
        print('Error during command line parsing: {0}'.format(str(e)))
        sys.exit(1)

if __name__ == '__main__':
    main()
