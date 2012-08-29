import javaLoggingHelper.config as config
import logging, settings
import javaLoggingHelper.backupService as backupService
from javaLoggingHelper.parsing import javaParser
from javaLoggingHelper.writing import javaWriter
import os
import sys

_logger = logging.getLogger(settings.LOGGER_NAME)

def main():
    applicationStart()
    
    for subdir, dirs, files in os.walk(settings.DATA_DIR):
        for f in files:
            fileToOpen = subdir + '/' + f
            f = open(fileToOpen, 'r')
            parsingResult = javaParser.parseFile(f)
            f.close()
            
            f = open(fileToOpen, 'r+')
            javaWriter.writeLoggingMessages(f, parsingResult)
            f.close()
            
    applicationEnd()
    
def applicationStart():
    config.configureLogging()
    config.clearLog()
    
    _logger.info('Application started.')
    
    args = sys.argv[1:]
    while len(args) > 0:
        currentArg = args[0]

        if currentArg == '--root' or currentArg == '-r':
            projectRootPath = args[1]
            settings.DATA_DIR = projectRootPath
            args = args[2:]
        else:
            print 'Unknown argument: %r' % args[0]
            args = args[1:]
       
    if not settings.DATA_DIR:
        raise Exception('Project root path not specified.')
        
    backupService.recoverDataFromBackup()
    backupService.backupADirectory(settings.DATA_DIR)
    
def applicationEnd():
    _logger.info('Application ended.')
    
