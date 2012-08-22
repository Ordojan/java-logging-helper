from javaLoggingHelper import backupService, config

if __name__ == '__main__':
    config.configureLogging()
    config.clearLog()
    
    backupService.recoverDataFromBackup()