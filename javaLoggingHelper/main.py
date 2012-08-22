import javaLoggingHelper.config as config
import logging, settings
import javaLoggingHelper.backupService as backupService
from javaLoggingHelper.parsing import javaParser
from javaLoggingHelper.writing import javaWriter
import os
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
    
