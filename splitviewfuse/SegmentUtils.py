import re

class SegmentUtils(object):
    
    SEGMENT_SEPARATOR = '.seg.'
    
    @staticmethod
    def splitSegmentPath(path):
        match = re.match('^(.*?)(' + re.escape(SegmentUtils.SEGMENT_SEPARATOR) + '([0-9]+))?$', path)
        filePath = match.groups()[0]
        segmentNumber = match.groups()[2]
        if segmentNumber is not None:
            segmentNumber = int(segmentNumber)
        return filePath, segmentNumber
    
    @staticmethod
    def joinSegmentPath(segmentName, segmentNumber):
        if segmentNumber is None:
            return segmentName
        return segmentName + SegmentUtils.SEGMENT_SEPARATOR + str(segmentNumber)