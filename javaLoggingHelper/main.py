import javaLoggingHelper.config as config
import logging, os, settings, sys, shutil

logger = logging.getLogger(settings.LOGGER_NAME)

def main():
    applicationStart()
    
    
    applicationEnd()
    
def applicationStart():
    config.configureLogging()
    
    if not os.path.exists(settings.TEST_DATA_DIR):
        logger.critical("Test data directory could not be found. Application terminated.")
        sys.exit()
        
    if not os.path.exists(settings.TEST_DATA_BACKUP_DIR):
        shutil.copytree(settings.TEST_DATA_DIR, settings.TEST_DATA_BACKUP_DIR)
    
    
def applicationEnd():
    logger.info('Application end.')
    
    
    