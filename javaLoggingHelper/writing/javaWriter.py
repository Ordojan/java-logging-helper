import logging, settings

_logger = logging.getLogger(settings.LOGGER_NAME)


def enum(**enums):  
    return type('Enum', (), enums)

methodCallNames = enum(FINEST='finest', ENTERING='entering', EXITING='exiting')

class LogMessage(object):
    def __init__(self, loggerVariableName):
        self.loggerVariableName = loggerVariableName
        
    def __repr__(self):
        return 'LogMessage(loggerVariableName = {0})'.format(self.loggerVariableName)

class EnteringLogMessage(LogMessage):
    def __init__(self, loggerVariableName, className, methodName, parameters):
        super(EnteringLogMessage, self).__init__(loggerVariableName)
        self.methodCallName = methodCallNames.ENTERING
        self.className = className
        self.methodName = methodName
        self.parameters = parameters
    
    def getLoggingStatement(self):
        # tracer.entering(ChangeSetElement2.class.getSimpleName(), "getOrigin");
        # tracer.entering(ChangeSetElement2.class.getSimpleName(), "ChangeSetElement2", new Object[]{file, status});
        
        if len(self.parameters) > 0:
            formatedParameters = ''
            for param in self.parameters:
                formatedParameters = formatedParameters + param + ', '
            formatedParameters = formatedParameters[:len(formatedParameters) - 2]
            
            return '{0}.{1}({2}.class.getSimpleName(), "{3}", new Object[]{{4}})'.format(self.loggerVariableName, self.methodCallName, self.className, self.methodName, formatedParameters)
        else:
            return '{0}.{1}({2}.class.getSimpleName(), "{3}")'.format(self.loggerVariableName, self.methodCallName, self.className, self.methodName)
            
    def __repr__(self):
        return 'EnteringLogMessage(loggerVariableName = {0}, className = {1}, methodName = {2}, parameters = {3})'.format(self.loggerVariableName, self.className, self.methodName, self.parameters)
    
class ExitingLogMessage(LogMessage):
    def __init__(self, loggerVariableName, className, methodName, parameter):
        super(ExitingLogMessage, self).__init__(loggerVariableName)
        self.methodCallName = methodCallNames.EXITING
        self.className = className
        self.methodName = methodName
        self.parameter = parameter
    
    def getLoggingStatement(self):
        # tracer.exiting(ChangeSetElement2.class.getSimpleName(), "ChangeSetElement2", file);
        
        if len(self.parameter) > 0:
            return '{0}.{1}({2}.class.getSimpleName(), "{3}", {4})'.format(self.loggerVariableName, self.methodCallName, self.className, self.methodName, self.parameter)
        else:
            return '{0}.{1}({2}.class.getSimpleName(), "{3}")'.format(self.loggerVariableName, self.methodCallName, self.className, self.methodName)
            
    def __repr__(self):
        return 'ExitingLogMessage(loggerVariableName = {0}, className = {1}, methodName = {2}, parameter = {3})'.format(self.loggerVariableName, self.className, self.methodName, self.parameter)
    
def writeLoggingMessages(javaParsingResult):
    _logger.info('Entering writeLoggingMessages {0}'.format(javaParsingResult))
    
    
    _logger.info('Exiting writeLoggingMessages {0}'.format(javaParsingResult))
