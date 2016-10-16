from fuse import FUSE
from splitviewfuse import SplitViewFuseBase

from splitviewfuse.SegmentUtils import SegmentUtils
from splitviewfuse.filehandlecontainers.VirtualRegularFileFileHandleContainer import VirtualRegularFileFileHandleContainer
import sys
from splitviewfuse.SplitViewFuseBase import ArgumentParserError
from argparse import ArgumentTypeError


class UnionViewFuse(SplitViewFuseBase.SplitViewFuseBase):
    
    def __init__(self, root, maxSegmentSize, loglevel, logfile):
        super(UnionViewFuse, self).__init__(root, maxSegmentSize, VirtualRegularFileFileHandleContainer(maxSegmentSize), loglevel, logfile)

    def _SplitViewFuseBase__processReadDirEntry(self, absRootPath, entry):
        dirContent = list()
        segmentFreeEntry, segmentNumber = SegmentUtils.splitSegmentPath(entry)
        if segmentNumber is None or segmentNumber is 0:
            dirContent.append(segmentFreeEntry)
        return dirContent


def main():
    try:
        args = SplitViewFuseBase.parseArguments(sys.argv, 'Filesystem that merges segmented files into complete ones. The size is specified in the mount options.')
        _ = FUSE(UnionViewFuse(args.device, args.mountOptions['segmentsize'], args.mountOptions['loglevel'], args.mountOptions['logfile']), args.dir, **args.mountOptions['other'])
        #fuse = FUSE(UnionViewFuse(args.device, args.mountOptions['segmentsize']), args.dir, nothreads=True, foreground=True)
    except ArgumentParserError as e:
        print('Error during command line parsing: {0}'.format(str(e)))
        sys.exit(1)
    except ArgumentTypeError as e:
        print('Error during command line parsing: {0}'.format(str(e)))
        sys.exit(1)

if __name__ == '__main__':
    main()
