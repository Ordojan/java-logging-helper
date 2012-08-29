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
    
    backupService.recoverDataFromBackup()
    backupService.backupADirectory(settings.DATA_DIR)
    
def applicationEnd():
    _logger.info('Application ended.')
    
def parseArgs():
    args = sys.argv[:]  # Copy so don't destroy original
    while len(args) > 0:
        current_arg = args[0]

        if current_arg == '-f':
            foo = args[1]
            args = args[2:]
        elif current_arg == '-b':
            bar = args[1]
            args = args[2:]
        elif current_arg == '-z':
            baz = args[1]
            args = args[2:]
        else:
            print 'Unknown argument: %r' % args[0]
            args = args[1:]
