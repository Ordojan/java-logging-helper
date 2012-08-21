import shutil, os, logging, settings

_logger = logging.getLogger(settings.LOGGER_NAME)

def backupADirectory(directory):
    _logger.info('Entering backupADirectory {0}'.format(directory))

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