from LoggingUtils import LoggingUtil
from abc import ABCMeta, abstractmethod
from argparse import ArgumentParser, ArgumentTypeError, Action
from errno import EACCES, EPERM, ENOENT, EBADFD
from fuse import FuseOSError, Operations, LoggingMixIn
import logging, os, stat


class SplitViewFuseBase(LoggingMixIn, Operations):
    
    __metaclass__ = ABCMeta
    
    
    def __init__(self, root, maxFileSize, fileHandleContainer, logLevel = None, logFile = None):
        LoggingUtil.initialize(logLevel, logFile)
        self.logger = LoggingUtil.getLogger(SplitViewFuseBase)
        self.root = os.path.realpath(root)
        self.maxFileSize = maxFileSize
        self.fileHandleContainer = fileHandleContainer

    def __call__(self, op, path, *args):
        return super(SplitViewFuseBase, self).__call__(op, path, *args)
    
    def __getAbsolutePath(self, path):
        absRootPath = self.root + path
        if os.path.islink(absRootPath):
            return os.path.realpath(absRootPath)
        return absRootPath
   
    @abstractmethod
    def __processReadDirEntry(self, absRootPath, entry):
        '''
        Returns the view entries that shall be displayed for the given entry
        '''

    def access(self, path, mode):
        if mode & os.W_OK != 0:
            raise FuseOSError(EACCES)
            
        pathToTest = self.__getAbsolutePath(path)
        if not os.path.isdir(pathToTest):
            with self.fileHandleContainer.createHandleObject(pathToTest) as virtualFile:
                pathToTest = virtualFile.getPath()
        
        if not os.access(pathToTest, mode):
            raise FuseOSError(EACCES)

    def chmod(self, path, mode):
        raise FuseOSError(EPERM)

    def chown(self, path, uid, gid):
        raise FuseOSError(EPERM)

    def create(self, path, mode):
        raise FuseOSError(EPERM)

    def flush(self, path, fh):
        # we do not support writing, so we ignore this call
        return

    def fsync(self, path, datasync, fh):
        # we do not support writing, so we ignore this call
        return

    def getattr(self, path, fh=None):
        absRootPath = self.__getAbsolutePath(path)
    
        st = None
        size = None
        
        if os.path.isdir(absRootPath):
            st = os.lstat(absRootPath)
            size = st.st_size
        else:
            try:
                with self.fileHandleContainer.createHandleObject(absRootPath) as virtualFile:
                    st = os.lstat(virtualFile.getPath())
                    size = virtualFile.size()
            except ValueError:
                raise FuseOSError(ENOENT)

        stats = dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        stats['st_mode'] = st.st_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
        stats['st_size'] = size

        return stats
        
    getxattr = None

    def link(self, target, source):
        raise FuseOSError(EPERM)

    listxattr = None
    
    def mknod(self, path, mode, dev):
        raise FuseOSError(EPERM)
    
    def mkdir(self, path, mode):
        raise FuseOSError(EPERM)

    def open(self, path, flags):
        if flags & (os.O_CREAT | os.O_APPEND | os.O_RDWR | os.O_WRONLY) != 0:
            raise FuseOSError(EPERM)
        absRootPath = self.__getAbsolutePath(path)
        try:
            return self.fileHandleContainer.registerHandle(absRootPath)
        except ValueError:
            raise FuseOSError(ENOENT)

    def read(self, path, size, offset, fh):
        try:
            virtualFile = self.fileHandleContainer.getHandle(fh)
            return virtualFile.read(offset, size)
        except ValueError:
            raise FuseOSError(EBADFD)
        
    def readdir(self, path, fh):
        dirContent = ['.', '..']
        absRootPath = self.__getAbsolutePath(path)
        for entry in os.listdir(absRootPath):
            dirContent.extend(self.__processReadDirEntry(absRootPath, entry))
        return dirContent

    def readlink(self, path):
        raise FuseOSError(EPERM)

    def release(self, path, fh):
        self.fileHandleContainer.unregisterHandle(fh)

    def rename(self, old, new):
        raise FuseOSError(EPERM)
    
    def rmdir(self, path):
        raise FuseOSError(EPERM)

    def statfs(self, path):
        # TODO try to calculate useful information
        stv = os.statvfs(self.__getAbsolutePath(path))
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def symlink(self, target, source):
        raise FuseOSError(EPERM)

    def truncate(self, path, length, fh=None):
        raise FuseOSError(EPERM)

    def unlink(self, path):
        raise FuseOSError(EPERM)

    def utimens(self, path, times=None):
        raise FuseOSError(EPERM)

    def write(self, path, data, offset, fh):
        raise FuseOSError(EPERM)






class FullPaths(Action):
    """Expand user- and relative-paths"""
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, os.path.abspath(os.path.expanduser(values)))
        
class MountOptions(Action):
    
    LOGLEVELS = {"debug" : logging.DEBUG, "info" : logging.INFO, "warn" : logging.WARN, "error" : logging.ERROR}
    
    def __call__(self, parser, namespace, values, option_string=None):
        resultObject = dict()
        options = values
        
        resultObject["segmentsize"] = int(MountOptions.__determineKeyValueOption__(options, "segmentsize")[1])
        if resultObject["segmentsize"] < 1:
            raise ArgumentParserError("The given maximum segment size is invalid because it is less than 1.")
        
        resultObject["loglevel"] = MountOptions.__convert_to_loglevel(MountOptions.__determineKeyValueOption__(options, "loglevel")[1])
        resultObject["logfile"] = MountOptions.__determineKeyValueOption__(options, "logfile")[1]

        interestingOptions = ["segmentsize=", "loglevel=", "logfile="]
        filteredOptions = filter(lambda x: not any(x.startswith(string) for string in interestingOptions), options)
        otherOptions = dict()
        for option in filteredOptions:
            parts = option.split('=')
            if len(parts) == 1:
                otherOptions[parts[0]] = True
            else:
                otherOptions[parts[0]] = parts[1]
        resultObject["other"] = otherOptions

        setattr(namespace, self.dest, resultObject)
        
    @staticmethod
    def __determineKeyValueOption__(options, name):
        for option in options:
            keyString = name + "="
            if option.startswith(keyString):
                return name, option[len(keyString):]
            if option == name:
                return name, None
        return None, None
    
    @staticmethod        
    def are_mount_options(options):
        optionList = options.split(',')
        
        if "" in optionList:
            raise ArgumentTypeError("Empty option given.")
        
        _, maxFileSize = MountOptions.__determineKeyValueOption__(optionList, "segmentsize")
        if maxFileSize is None:
            raise ArgumentTypeError("The segment size option is mandatory.")
        if not maxFileSize.isdigit():
            raise ArgumentTypeError("The segment size has to be a number.")
        
        logFileKey, logFile = MountOptions.__determineKeyValueOption__(optionList, "logfile")
        if logFileKey is not None and (logFile is None or logFile == ""):
            raise ArgumentTypeError("You have to specify a log file path if you use the logfile option.")
        
        logLevelKey, logLevel = MountOptions.__determineKeyValueOption__(optionList, "loglevel")
        if logLevelKey is not None and MountOptions.__convert_to_loglevel(logLevel) is None:
            raise ArgumentTypeError("The given log level is invalid. Use one of {} instead.".format(", ".join(MountOptions.LOGLEVELS.keys())))
        
        return optionList
    
    @staticmethod
    def __convert_to_loglevel(value):
        if not MountOptions.LOGLEVELS.has_key(value):
            return None
        return MountOptions.LOGLEVELS.get(value)
        
def __are_mount_options(options):
    return MountOptions.are_mount_options(options)
     
def __is_dir(dirname):
    """Checks if a path is an actual directory"""
    if not os.path.isdir(dirname):
        msg = "{0} is not a directory".format(dirname)
        raise ArgumentTypeError(msg)
    else:
        return dirname
    

class ArgumentParserError(Exception): pass
class __ThrowingArgumentParser(ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)

def parseArguments(args, descriptionText='Filesystem'):
    '''
    Parses the arguments received from the command line.
    Do not modify the argument count or order. This function needs the first parameter
    indicating the executed program to succeed.
    '''
    parser = __ThrowingArgumentParser(description=descriptionText)
    parser.add_argument('device', action=FullPaths, type=__is_dir, help='the document root for the original files')
    parser.add_argument('dir', action=FullPaths, type=__is_dir, help='the mount point')    
    # workaround for Issue 9694 (https://bugs.python.org/issue9694)
    requiredArguments = parser.add_argument_group('required arguments')
    requiredArguments.add_argument("-o", action=MountOptions, type=__are_mount_options, required=True, dest='mountOptions', help='mount options as used in /etc/fstab. You have to specify the additional option "segmentsize=<size in bytes>".')
    
    return parser.parse_args(args[1:])

