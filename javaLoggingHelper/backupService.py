import os, logging, settings
import shutil

_logger = logging.getLogger(settings.LOGGER_NAME)

def makeBackup():
    backupADirectory(settings.DATA_DIR)

def backupADirectory(directory):
    _logger.info('Entering backupADirectory %s' % directory)

    if not os.path.exists(directory):
        _logger.critical("Directory not found.")
        raise IOError('Directory not found.')
    
    if directory.endswith('/'):
        directory = directory[:len(directory) - 1]
    
    backupDirectory = directory + '_backup'
    
    if os.path.exists(backupDirectory):
        shutil.rmtree(backupDirectory) 
        
    shutil.copytree(directory, backupDirectory)
    
    if not os.path.exists(backupDirectory):
        _logger.critical("Backup could not be created.")
        raise IOError('Backup could not be created.')
    
    _logger.info('Exiting backupADirectory')
    
def recoverDataFromBackup():
    _logger.info('Entering recoverFromBackup')
    
    directory = settings.DATA_DIR
    
    if directory.endswith('/'):
        directory = directory[:len(directory) - 1]
    
    backupDirectory = directory + '_backup'
    
    if not os.path.exists(backupDirectory):
        _logger.critical("Backup directory not found.")
        raise IOError('Backup directory could not found.')
    
    if os.path.exists(directory):
        shutil.rmtree(directory) 
    
    shutil.copytree(backupDirectory, directory)
    
    if not os.path.exists(directory):
        _logger.critical("Data could not be recovered not be created.")
        raise IOError('Data could not be recovered not be created.')
    
    _logger.info('Exiting recoverFromBackup')
