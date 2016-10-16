import logging

class LoggingUtil(object):

    @staticmethod
    def initialize(logLevel = logging.INFO, filePath = None):
        if file is not None:
            logging.basicConfig(filename=filePath, filemode='w', level=logLevel)
        else:
            logging.basicConfig(level=logLevel)

    @staticmethod
    def getLogger(clazz = None):
        if clazz is not None:
            return logging.getLogger(clazz.__name__)
        return logging.getLogger(clazz)
