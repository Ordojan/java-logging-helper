import logging
import settings

def clearLog():
    f = open(settings.LOG_FILE_DIR, 'w')
    f.close()
    
def configureLogging():
    # setting the level to debug for the root _logger
    logging.getLogger(settings.LOGGER_NAME).setLevel(logging.DEBUG)
    
    # create console handler and set level to warning
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)

    # create console RotatingFileHandler and set level to debug
    logFilePath = settings.LOG_FILE_DIR
    
    fileHandler = logging.FileHandler(logFilePath)
    fileHandler.setLevel(logging.DEBUG)
    
    # create formatter
    consoleFormatter = logging.Formatter('%(levelname)-10s %(message)s')
    fileFormatter = logging.Formatter('%(levelname)-10s %(message)s')
    
    # add formatter to handlers
    consoleHandler.setFormatter(consoleFormatter)
    fileHandler.setFormatter(fileFormatter)
    
    # add handlers to root _logger
    _logger = logging.getLogger(settings.LOGGER_NAME)
    if settings.LOGGING_FILE_HANDLER:
        _logger.addHandler(fileHandler)
    if settings.LOGGING_CONSOLE_HANDLER:
        _logger.addHandler(consoleHandler)
    
#    if not settings.LOGGING_FILE_HANDLER and not settings.LOGGING_CONSOLE_HANDLER:
#        dummyHandler = logging.PlaceHolder
#        _logger.addHandler(dummyHandler)
        
