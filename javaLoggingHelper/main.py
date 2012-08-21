import javaLoggingHelper.config as config
import logging, settings
import javaLoggingHelper.backupService as backupService
from javaLoggingHelper.parsing import javaParser
from javaLoggingHelper.writing import javaWriter

_logger = logging.getLogger(settings.LOGGER_NAME)

def main():
    applicationStart()
    
    f = open(settings.TEST_DATA_DIR + '/' + settings.TEST_DATA_FILENAME, 'r')
    parsingResult = javaParser.parseFile(f)
    f.close()
    
    f = open(settings.TEST_DATA_DIR + '/' + settings.TEST_DATA_FILENAME, 'r+')
    javaWriter.writeLoggingMessages(f, parsingResult)
    f.close()
    
    applicationEnd()
    
def applicationStart():
    config.configureLogging()
    clearLog()
    
    _logger.info('Application started.')
    
    backupService.backupADirectory(settings.TEST_DATA_DIR)
        
def applicationEnd():
        
    _logger.info('Application ended.')
    
def clearLog():
    f = open(settings.LOG_FILE_DIR, 'w')
    f.write('')
    f.close()