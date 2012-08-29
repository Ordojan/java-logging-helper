import os

PROJECT_ROOT_DIR = os.path.dirname(__file__)

DATA_DIR = PROJECT_ROOT_DIR + '/testData'
TEST_DATA_BACKUP_DIR = DATA_DIR + '/backups'
TEST_DATA_FILENAME = 'Test.java'

LOG_FILE_DIR = './app.log'

LOGGING_FILE_HANDLER = False
LOGGING_CONSOLE_HANDLER = True

LOGGER_NAME = 'JavaLoggingHelper'

JAVA_LOGGER_VARIABLE_NAME = 'tracer'
JAVA_LOGGER_NAME = 'Config.GLOBAL_LOGGER_NAME'
JAVA_LOGGER_CLASS = 'java.util.logging.Logger'
JAVA_OUTPUT_VARIABLE_NAME = '_output_'

INDENT = '    '
