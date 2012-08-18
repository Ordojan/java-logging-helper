import logging
import settings

def configureLogging():
    # setting the level to debug for the root logger
    logging.getLogger(settings.LOGGER_NAME).setLevel(logging.DEBUG)
    
    # create console handler and set level to warning
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)

    # create console RotatingFileHandler and set level to debug
    logFilePath = './app.log'
    
    fileHandler = logging.FileHandler(logFilePath)
    fileHandler.setLevel(logging.DEBUG)
    
    # create formatter
    consoleFormatter = logging.Formatter('%(levelname)-10s %(message)s')
    fileFormatter = logging.Formatter('%(levelname)-10s %(message)s')
    
    # add formatter to handlers
    consoleHandler.setFormatter(consoleFormatter)
    fileHandler.setFormatter(fileFormatter)
    
    # add handlers to root logger
    logger = logging.getLogger(settings.LOGGER_NAME)
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)
        