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
            
            return "{0}.{1}({2}.class.getSimpleName(), \"{3}\", new Object[]{{{4}}});\n".format(self.loggerVariableName, self.methodCallName, self.className, self.methodName, formatedParameters)
        else:
            return '{0}.{1}({2}.class.getSimpleName(), "{3}");\n'.format(self.loggerVariableName, self.methodCallName, self.className, self.methodName)
            
    def __repr__(self):
        return 'EnteringLogMessage(loggerVariableName = {0}, className = {1}, methodName = {2}, parameters = {3})'.format(self.loggerVariableName, self.className, self.methodName, self.parameters)
    
class ExitingLogMessage(LogMessage):
    def __init__(self, loggerVariableName, className, operationName, parameter):
        super(ExitingLogMessage, self).__init__(loggerVariableName)
        self.methodCallName = methodCallNames.EXITING
        self.className = className
        self.operationName = operationName
        self.parameter = parameter
    
    def getLoggingStatement(self):
        # tracer.exiting(ChangeSetElement2.class.getSimpleName(), "ChangeSetElement2", file);
        
        if len(self.parameter) > 0:
            return '{0}.{1}({2}.class.getSimpleName(), "{3}", {4});\n'.format(self.loggerVariableName, self.methodCallName, self.className, self.operationName, self.parameter)
        else:
            return '{0}.{1}({2}.class.getSimpleName(), "{3}");\n'.format(self.loggerVariableName, self.methodCallName, self.className, self.operationName)
            
    def __repr__(self):
        return 'ExitingLogMessage(loggerVariableName = {0}, className = {1}, operationName = {2}, parameter = {3})'.format(self.loggerVariableName, self.className, self.operationName, self.parameter)
    
def writeLoggingMessages(fileToWriteTo, javaParsingResult):
    _logger.info('Entering writeLoggingMessages {0}'.format(javaParsingResult))
    
    fileContents = fileToWriteTo.readlines()
    
    if javaParsingResult.constructorDefinitions:
        for definition in javaParsingResult.constructorDefinitions:
            className = javaParsingResult.classDefinition.name
            operationName = definition.name
            
            parameterValues = []
            for param in definition.parameters:
                parameterValues.append(param.value)
                
            enteringLogMessage = EnteringLogMessage('tracer', className, operationName, parameterValues)
            
            fileContents.insert(definition.lineNumber, enteringLogMessage.getLoggingStatement())
            
            exitingLogMessage = ExitingLogMessage('tracer', className, operationName, [])
            
            fileContents.insert(definition.endLineNumber, exitingLogMessage.getLoggingStatement())
    
    fileToWriteTo.seek(0)
    fileToWriteTo.writelines(fileContents)
    
    _logger.info('Exiting writeLoggingMessages {0}'.format(javaParsingResult))
