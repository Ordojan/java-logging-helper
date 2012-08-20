import javaLoggingHelper.config as config
import logging, os, settings, sys, shutil
from javaLoggingHelper.parsing import javaParser

_logger = logging.getLogger(settings.LOGGER_NAME)

def main():
    applicationStart()
    
    f = open(settings.TEST_DATA_DIR + '/' + settings.TEST_DATA_FILENAME)
    parsingResult = javaParser.findDefinitions(f)
    print parsingResult
    f.close()
    
    applicationEnd()
    
def applicationStart():
    config.configureLogging()
    clearLog()
    
    _logger.info('Application started.')
    
    if not os.path.exists(settings.TEST_DATA_DIR):
        _logger.critical("Test data directory could not be found. Application terminated.")
        sys.exit()
        
    if os.path.exists(settings.TEST_DATA_BACKUP_DIR):
        _logger.info("Test data backup directory already exists. Deleting directory.")
        shutil.rmtree(settings.TEST_DATA_BACKUP_DIR)
    
    _logger.info("Copying test data from {0} to {1}".format(os.path.abspath(settings.TEST_DATA_DIR), os.path.abspath(settings.TEST_DATA_BACKUP_DIR)))
    shutil.copytree(settings.TEST_DATA_DIR, settings.TEST_DATA_BACKUP_DIR)
    
def applicationEnd():
    if os.path.exists(settings.TEST_DATA_BACKUP_DIR):
        _logger.info("Deleting test data backup directory.")
        shutil.rmtree(settings.TEST_DATA_BACKUP_DIR)
        
    _logger.info('Application ended.')
    
def clearLog():
    f = open(settings.LOG_FILE_DIR, 'w')
    f.write('')
    f.close()