import logging, settings, re, os

_logger = logging.getLogger(settings.LOGGER_NAME) 

class JavaParsingResult(object):
    def __init__(self, classDefinition, constructorDefinitions, methodDefinitions):
        self.classDefinition = classDefinition
        self.constructorDefinitions = constructorDefinitions
        self.methodDefinitions = methodDefinitions

    def __repr__(self):
        return 'JavaParsingResult(classDefinition = {0}, constructorDefinitions = {1}, methodDefinitions = {2})'.format(self.classDefinition, self.constructorDefinitions, self.constructorDefinitions)
    
class Definition(object):
    def __init__(self, name, lineNumber):
        self.lineNumber = lineNumber
        self.endLineNumber = None
        self.name = name
        
    def __repr__(self):
        return 'Definition(name = {0}, lineNumber = {1}, endLineNumber = {2})'.format(self.name, self.lineNumber, self.endLineNumber)
    
class ClassDefinition(Definition):
    def __init__(self, name, lineNumber):
        super(ClassDefinition, self).__init__(name, lineNumber)
        
    def __repr__(self):
        return 'ClassDefinition(name = {0}, lineNumber = {1}, endLineNumber = {2})'.format(self.name, self.lineNumber, self.endLineNumber)
        
class MethodDefinition(Definition):
    def __init__(self, returnValue, name, parameters, lineNumber):
        super(MethodDefinition, self).__init__(name, lineNumber)
        self.returnStatements = []
        self.returnValue = returnValue
        self.parameters = parameters
        
    def __repr__(self):
        return 'MethodDefinition(returnValue = {0}, name = {1}, parameters = {2}, returnStatements = {3}, lineNumber = {4}, endLineNumber = {5})'.format(self.returnValue, self.name, self.parameters, self.returnStatements, self.lineNumber, self.endLineNumber) 

class ConstructorDefinition(Definition):
    def __init__(self,  name, parameters, lineNumber):
        super(ConstructorDefinition, self).__init__(name, lineNumber)
        self.parameters = parameters
        
    def __repr__(self):
        return 'ConstructorDefinition(name = {0}, parameters = {1}, lineNumber = {2}, endLineNumber = {3})'.format(self.name, self.parameters, self.lineNumber, self.endLineNumber) 
    
class Parameter(object):
    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value
        
    def __repr__(self):
        return 'Parameter(type_ = {0}, value = {1})'.format(self.type_, self.value) 
    
class ReturnStatement(object):
    def __init__(self, value, lineNumber):
        self.value = value
        self.lineNumber = lineNumber
        
    def __repr__(self):
        return 'ReturnStatement(value = {0}, lineNumber = {1})'.format(self.value, self.lineNumber) 

class FileLine(object):
    def __init__(self, text, lineNumber):
        self.text = text
        self.lineNumber = lineNumber
       
    def __repr__(self):
        text = self.text.strip('\n')
        return 'FileLine(text = {0}, lineNumber = {1})'.format(text, self.lineNumber)          

class File(object):
    def __init__(self, file_):
        self.fileName = file_.name
        self.fileLines = []
        self.lineIndex = 0
        
        textFileLines = file_.readlines()

        for line in textFileLines:
            lineNumber = textFileLines.index(line) + 1
            fileLine = FileLine(line, lineNumber)
        
            self.fileLines.append(fileLine)
            
    def getCurrentFileLine(self):
        if self.lineIndex < len(self.fileLines):
            return self.fileLines[self.lineIndex]
        else:
            return None
    
    def setCurrentFileLineLocation(self, lineNumber):
        self.lineIndex = lineNumber - 1 
    
    def moveToNextLine(self):
        self.lineIndex = self.lineIndex + 1
        
    def __repr__(self):
        return 'File(file_ = {0})'.format(self.fileName)       

_visibilities = ('public', 'protected', 'private')

def parseFile(file_):
    _logger.info('Entering findDefinitions {0}'.format(repr(file_)))
    
    fileToParse = File(file_)
    
    classDefinition = None
    constructorDefinitions = []
    methodDefinitions = []
    
    while fileToParse.getCurrentFileLine() is not None:
        result = _searchForClassDefinition(fileToParse)
        
        if result:
            _logger.info('Class definition found {0}'.format(result))
            
            classDefinition = result
        else:
            result = _searchForOperationDefinition(fileToParse)
            
            if result:
                _logger.info('Operation definition found {0}'.format(result))
                
                if isinstance(result, ConstructorDefinition):
                    constructorDefinitions.append(result)
                elif isinstance(result, MethodDefinition):
                    methodDefinitions.append(result)
                    
        fileToParse.moveToNextLine()
        
    javaParsingResult = JavaParsingResult(classDefinition, constructorDefinitions, methodDefinitions)
    
    _logger.info('Exiting findDefinitions {0}'.format(javaParsingResult))
    
    return javaParsingResult

def _searchForClassDefinition(fileToParse):
    _logger.info('Entering _searchForClassDefinition {0}'.format(fileToParse))
    
    fileLine = fileToParse.getCurrentFileLine()
    
    match = re.search(r'(?:(?:public)|(?:private)|(?:static)|(?:protected)\s+)*(class) (\w+)', fileLine.text)
    
    output = None
    if match:
        className = match.groups()[1]
        classDefinition = ClassDefinition(className, fileLine.lineNumber)
        _findEndOfDefinition(fileToParse, classDefinition)
        
        output = classDefinition
        
    _logger.info('Exiting _searchForClassDefinition {0}'.format(output))
    
    return output

def _searchForOperationDefinition(fileToParse):
    _logger.info('Entering _searchForOperationDefinition {0}'.format(fileToParse))
    
    fileLine = fileToParse.getCurrentFileLine()
    
    match = re.search(r'(\w+)\W(\w+)\((.*)\)', fileLine.text)
    output = None
    
    if not match:
        _logger.info('Exiting _searchForOperationDefinition {0}'.format(output))
        
        return output
        
    matchGroup = match.groups()
    
    if _isConstructorDefinition(matchGroup):
        name = matchGroup[1]
        parameters = _findParameters(matchGroup[2])
        lineNumber = fileLine.lineNumber
        
        constructorDefinition = ConstructorDefinition(name, parameters, lineNumber)
        _findEndOfDefinition(fileToParse, constructorDefinition)
        
        output = constructorDefinition
    elif _isMethodDefinition(matchGroup):
        returnValue = matchGroup[0]
        name = matchGroup[1]
        parameters = _findParameters(matchGroup[2])
        lineNumber = fileLine.lineNumber
        
        methodDefinition = MethodDefinition(returnValue, name, parameters, lineNumber)
        _findEndOfDefinition(fileToParse, methodDefinition)
        
        output = methodDefinition
    
    _logger.info('Exiting _searchForOperationDefinition {0}'.format(output))
    
    return output
    
def _findEndOfDefinition(fileToParse, definition):
    _logger.info('Entering _findEndOfOperation {0} {1}'.format(fileToParse, definition))
    
    startingLineNumber = fileToParse.getCurrentFileLine().lineNumber
    
    curlyBraceStack = []
    openBrace = '{'
    closeBrace = '}'
    
    while fileToParse.getCurrentFileLine() is not None:
        fileLine = fileToParse.getCurrentFileLine()
        
        if openBrace in fileLine.text:
            curlyBraceStack.append(openBrace)
        elif closeBrace in fileLine.text:
            curlyBraceStack.pop()
            
        if isinstance(definition, MethodDefinition):
            returnStatement = _searchForReturnStatement(fileLine)
            if returnStatement:
                definition.returnStatements.append(returnStatement)
                        
        if len(curlyBraceStack) is 0:
            _logger.info('Exiting _findEndOfOperation')
            
            definition.endLineNumber = fileLine.lineNumber
            break
        
        fileToParse.moveToNextLine()
        
    if isinstance(definition, ClassDefinition):
        fileToParse.setCurrentFileLineLocation(startingLineNumber)
        
def _searchForReturnStatement(fileLine):
    returnStatement = 'return'
    
    if returnStatement not in fileLine.text:
        return None
    
    match = re.search(r'(return)([^;]*)', fileLine.text)
    
    if not match:
        return None
    
    matchGroup = match.groups()
    value = matchGroup[1].strip()
    
    return ReturnStatement(value, fileLine.lineNumber)
            
def _isMethodDefinition(matchGroup):
    _logger.info('Entering _isMethodDefinition {0}'.format(matchGroup))
    
    output = False

    if matchGroup[0] not in _visibilities:
        output = True
        
    _logger.info('Exiting _isMethodDefinition {0}'.format(output))

    return output

def _isConstructorDefinition(matchGroup):
    _logger.info('Entering _isContructorDefinition {0}'.format(matchGroup))

    output = False
    
    if matchGroup[0] in _visibilities:
        output = True
    
    _logger.info('Exiting _isContructorDefinition {0}'.format(output))

    return output

def _findParameters(text):
    _logger.info('Entering _findParameters {0}'.format(repr(text))) 
                 
    parameters = []
    
    if text is []:
        _logger.info('Exiting _isContructorDefinition {0}'.format(repr(parameters)))
        
        return parameters
    
    parametersText = text.replace(',', '').split()
    
    
    for index in range(len(parametersText)):
        if index % 2 is 0:
            parameter = Parameter(None, None)
            parameter.type_ = parametersText[index]
        else:
            parameter.value = parametersText[index]
            parameters.append(parameter)
            
    _logger.info('Exiting _findParameters {0}'.format(repr(parameters)))
    
    return parameters