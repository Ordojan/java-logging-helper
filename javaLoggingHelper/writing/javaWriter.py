import logging, settings
import os

_logger = logging.getLogger(settings.LOGGER_NAME)

def enum(**enums):  
    return type('Enum', (), enums)

methodCallNames = enum(FINEST='finest', ENTERING='entering', EXITING='exiting')

class LogMessage(object):
    def __init__(self, loggerVariableName):
        self.loggerVariableName = loggerVariableName
        
    def __repr__(self):
        return 'LogMessage(loggerVariableName = %s)' % self.loggerVariableName

class LoggerVariableDeclaration(LogMessage):
    def __init__(self):
        super(LoggerVariableDeclaration, self).__init__(settings.JAVA_LOGGER_VARIABLE_NAME)
        self.javaLoggerClass = settings.JAVA_LOGGER_CLASS
        self.javaLoggerName = settings.JAVA_LOGGER_NAME
        
    def getLoggerDeclaration(self):
        return '%sprivate static %s %s = %s.getLogger(%s);\n' % settings.INDENT, self.javaLoggerClass, self.loggerVariableName, self.javaLoggerClass, self.javaLoggerName

class EnteringLogMessage(LogMessage):
    def __init__(self, loggerVariableName, className, methodName, parameters):
        super(EnteringLogMessage, self).__init__(loggerVariableName)
        self.methodCallName = methodCallNames.ENTERING
        self.className = className
        self.methodName = methodName
        self.parameters = parameters
    
    def getLoggingStatement(self, indentationLevel):
        indentation = indentationLevel * settings.INDENT
        if len(self.parameters) > 0:
            formatedParameters = ''
            for param in self.parameters:
                formatedParameters = formatedParameters + param + ', '
            formatedParameters = formatedParameters[:len(formatedParameters) - 2]
            
            return "%s%s.%s(%s.class.getSimpleName(), \"%s\", new Object[]{%s});\n\n" % indentation, self.loggerVariableName, self.methodCallName, self.className, self.methodName, formatedParameters
        else:
            return '%s%s.%s(%s.class.getSimpleName(), "%s");\n\n' % indentation, self.loggerVariableName, self.methodCallName, self.className, self.methodName
            
    def __repr__(self):
        return 'EnteringLogMessage(loggerVariableName = %s, className = %s, methodName = %s, parameters = %s)' % self.loggerVariableName, self.className, self.methodName, self.parameters
    
class ExitingLogMessage(LogMessage):
    def __init__(self, loggerVariableName, className, operationName, parameter):
        super(ExitingLogMessage, self).__init__(loggerVariableName)
        self.methodCallName = methodCallNames.EXITING
        self.className = className
        self.operationName = operationName
        self.parameter = parameter
    
    def getLoggingStatement(self, indentationLevel):
        indentation = indentationLevel * settings.INDENT
        
        if len(self.parameter) > 0:
            return '\n%s%s.%s(%s.class.getSimpleName(), "%s", %s);\n' % indentation, self.loggerVariableName, self.methodCallName, self.className, self.operationName, self.parameter
        else:
            return '\n%s%s.%s(%s.class.getSimpleName(), "%s");\n' % indentation, self.loggerVariableName, self.methodCallName, self.className, self.operationName
            
    def __repr__(self):
        return 'ExitingLogMessage(loggerVariableName = %s, className = %s, operationName = %s, parameter = %s)' % self.loggerVariableName, self.className, self.operationName, self.parameter

class LineOffset(object):
    def __init__(self):
        self.value = 0
    
    def incrementLineOffset(self):
        self.value = (self.value + 1)
    
    def decrementLineOffset(self):
        self.value = (self.value - 1)
        
    def __repr__(self):
        return 'LineOffset(value = %s)' % self.value
        
def writeLoggingMessages(fileToWriteTo, javaParsingResult):
    _logger.info('Entering writeLoggingMessages %s' % javaParsingResult)
    
    lineOffset = LineOffset()
    
    fileContents = fileToWriteTo.readlines()
    className = javaParsingResult.classDefinition.name
    
    if javaParsingResult.classDefinition:
        _writeJavaLoggerDeclarationToClassDefinition(fileContents, javaParsingResult.classDefinition, lineOffset)
        
        if javaParsingResult.constructorDefinitions:
            for definition in javaParsingResult.constructorDefinitions:
                _writeLoggingMessageToConstructorDefinition(fileContents, className, definition, lineOffset)
        if javaParsingResult.methodDefinitions:
            for definition in javaParsingResult.methodDefinitions:
                _writeLoggingMessageToMethodDefinition(fileContents, className, definition, lineOffset)
            
    fileToWriteTo.seek(0)
    fileToWriteTo.writelines(fileContents)
    
    _logger.info('Exiting writeLoggingMessages %s' % javaParsingResult)

def _writeLoggingMessageToConstructorDefinition(fileContents, className, constructorDefinition, lineOffset):
    operationName = constructorDefinition.name
    
    parameterValues = []
    for param in constructorDefinition.parameters:
        parameterValues.append(param.value)
        
    enteringLogMessage = EnteringLogMessage(settings.JAVA_LOGGER_VARIABLE_NAME, className, operationName, parameterValues)
    fileContents.insert((constructorDefinition.lineNumber + lineOffset.value), enteringLogMessage.getLoggingStatement(constructorDefinition.indentationLevel))
    lineOffset.incrementLineOffset()
    
    exitingLogMessage = ExitingLogMessage(settings.JAVA_LOGGER_VARIABLE_NAME, className, operationName, [])
    lineNumber = constructorDefinition.endLineNumber + (lineOffset.value - 1)
    fileContents.insert(lineNumber, exitingLogMessage.getLoggingStatement(constructorDefinition.indentationLevel))
    lineOffset.incrementLineOffset()
    
def _writeLoggingMessageToMethodDefinition(fileContents, className, methodDefinition, lineOffset):
    operationName = methodDefinition.name
    
    parameterValues = []
    for param in methodDefinition.parameters:
        parameterValues.append(param.value)
        
    enteringLogMessage = EnteringLogMessage(settings.JAVA_LOGGER_VARIABLE_NAME, className, operationName, parameterValues)
    fileContents.insert((methodDefinition.lineNumber + lineOffset.value), enteringLogMessage.getLoggingStatement(methodDefinition.indentationLevel))
    lineOffset.incrementLineOffset()
    
    if len(methodDefinition.returnStatements) is 0:
        exitingLogMessage = ExitingLogMessage(settings.JAVA_LOGGER_VARIABLE_NAME, className, operationName, [])
        lineNumber = methodDefinition.endLineNumber + (lineOffset.value - 1)
        fileContents.insert(lineNumber, exitingLogMessage.getLoggingStatement(methodDefinition.indentationLevel))
        lineOffset.incrementLineOffset()
    else:
        for returnStatement in methodDefinition.returnStatements:
            indentation = settings.INDENT * returnStatement.indentationLevel
            
            returnVariableDeclaration = '%s%s %s = %s;\n' % indentation, methodDefinition.returnValue, settings.JAVA_OUTPUT_VARIABLE_NAME, returnStatement.value
            lineNumberForReturnVariableDeclaration = returnStatement.lineNumber + (lineOffset.value - 1)
            fileContents.insert(lineNumberForReturnVariableDeclaration, returnVariableDeclaration)
            lineOffset.incrementLineOffset()
            
            exitingLogMessage = ExitingLogMessage(settings.JAVA_LOGGER_VARIABLE_NAME, className, operationName, settings.JAVA_OUTPUT_VARIABLE_NAME)
            lineNumber = returnStatement.lineNumber + (lineOffset.value - 1)
            fileContents.insert(lineNumber, exitingLogMessage.getLoggingStatement(returnStatement.indentationLevel))
            lineOffset.incrementLineOffset()
            
            returnMsg = '%sreturn %s;\n' % indentation, settings.JAVA_OUTPUT_VARIABLE_NAME
            lineNumber = returnStatement.lineNumber + lineOffset.value - 1
            
            del fileContents[lineNumber]
            lineOffset.decrementLineOffset()
            
            fileContents.insert(lineNumber, returnMsg)
            lineOffset.incrementLineOffset()
            
def _writeJavaLoggerDeclarationToClassDefinition(fileContents, definition, lineOffset):
    javaLoggerDeclaration = LoggerVariableDeclaration()

    fileContents.insert(definition.lineNumber, javaLoggerDeclaration.getLoggerDeclaration())
    lineOffset.incrementLineOffset()
