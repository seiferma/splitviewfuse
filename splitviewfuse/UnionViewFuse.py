from fuse import FUSE
from splitviewfuse import SplitViewFuseBase

from splitviewfuse.SegmentUtils import SegmentUtils
from splitviewfuse.filehandlecontainers.VirtualRegularFileFileHandleContainer import VirtualRegularFileFileHandleContainer


class UnionViewFuse(SplitViewFuseBase.SplitViewFuseBase):
    
    def __init__(self, root, maxSegmentSize):
        super(UnionViewFuse, self).__init__(root, maxSegmentSize, VirtualRegularFileFileHandleContainer(maxSegmentSize))

    def _SplitViewFuseBase__processReadDirEntry(self, absRootPath, entry):
        dirContent = list()
        segmentFreeEntry, segmentNumber = SegmentUtils.splitSegmentPath(entry)
        if segmentNumber is None or segmentNumber is 0:
            dirContent.append(segmentFreeEntry)
        return dirContent


def main():
    args = SplitViewFuseBase.parseArguments()
    _ = FUSE(UnionViewFuse(args.device, args.mountOptions['segmentsize']), args.dir, **args.mountOptions['other'])
    #fuse = FUSE(UnionViewFuse(args.device, args.mountOptions['segmentsize']), args.dir, nothreads=True, foreground=True)

if __name__ == '__main__':
    main()
