import logging, settings, re

_logger = logging.getLogger(settings.LOGGER_NAME) 

class JavaParsingResult(object):
    def __init__(self, classDefinition, constructorDefinitions, methodDefinitions):
        self.classDefinition = classDefinition
        self.constructorDefinitions = constructorDefinitions
        self.methodDefinitions = methodDefinitions

    def __repr__(self):
        return 'JavaParsingResult(classDefinition = %s, constructorDefinitions = %s, methodDefinitions = %s)' % (self.classDefinition, self.constructorDefinitions, self.constructorDefinitions)
    
class Definition(object):
    def __init__(self, name, lineNumber, indentationLevel):
        self.lineNumber = lineNumber
        self.endLineNumber = None
        self.name = name
        self.indentationLevel = indentationLevel
        
    def __repr__(self):
        return 'Definition(name = %s, lineNumber = %s, endLineNumber = %s)' % (self.name, self.lineNumber, self.endLineNumber)
    
class ClassDefinition(Definition):
    def __init__(self, name, lineNumber, indentationLevel):
        super(ClassDefinition, self).__init__(name, lineNumber, indentationLevel)
        
    def __repr__(self):
        return 'ClassDefinition(name = %s, lineNumber = %s, endLineNumber = %s)' % (self.name, self.lineNumber, self.endLineNumber)
        
class MethodDefinition(Definition):
    def __init__(self, returnValue, name, parameters, lineNumber, indentationLevel):
        super(MethodDefinition, self).__init__(name, lineNumber, indentationLevel)
        self.returnStatements = []
        self.returnValue = returnValue
        self.parameters = parameters
        
    def __repr__(self):
        return 'MethodDefinition(returnValue = %s, name = %s, parameters = %s, returnStatements = %s, lineNumber = %s, endLineNumber = %s)' % (repr(self.returnValue), self.name, repr(self.parameters), repr(self.returnStatements), self.lineNumber, self.endLineNumber) 

class ConstructorDefinition(Definition):
    def __init__(self,  name, parameters, lineNumber, indentationLevel):
        super(ConstructorDefinition, self).__init__(name, lineNumber, indentationLevel)
        self.parameters = parameters
        
    def __repr__(self):
        return 'ConstructorDefinition(name = %s, parameters = %s, lineNumber = %s, endLineNumber = %s)' % (self.name, self.parameters, self.lineNumber, self.endLineNumber)
    
class Parameter(object):
    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value
        
    def __repr__(self):
        return 'Parameter(type_ = %s, value = %s)' % (self.type_, self.value)
    
class ReturnStatement(object):
    def __init__(self, value, lineNumber, indentationLevel):
        self.value = value
        self.lineNumber = lineNumber
        self.indentationLevel = indentationLevel
        
    def __repr__(self):
        return 'ReturnStatement(value = %s, lineNumber = %s)' % (self.value, self.lineNumber)

class FileLine(object):
    def __init__(self, text, lineNumber):
        self.text = text
        self.lineNumber = lineNumber
        self.indentationLevel = 0
        
    def __repr__(self):
        text = self.text.strip('\n')
        return 'FileLine(text = %s, lineNumber = %s)'% (text, self.lineNumber)

class File(object):
    def __init__(self, file_):
        self.fileName = file_.name
        self.fileLines = []
        self.lineIndex = 0
        
        textFileLines = file_.readlines()

        for index in range(len(textFileLines)):
            lineNumber = index + 1
            fileLine = FileLine(textFileLines[index], lineNumber)
            
            originalLength = len(textFileLines[index])
            indentationLevel = originalLength - len(textFileLines[index].lstrip())
            fileLine.indentationLevel = indentationLevel
            
            self.fileLines.append(fileLine)
            
    def getCurrentFileLine(self):
        if self.lineIndex < len(self.fileLines):
            return self.fileLines[self.lineIndex]
        else:
            return None
    
    def setCurrentFileLineLocation(self, lineNumber):
        self.lineIndex = lineNumber
    
    def moveToNextLine(self):
        self.lineIndex = self.lineIndex + 1
        
    def __repr__(self):
        return 'File(file_ = %s)' % self.fileName       

_visibilities = ('public', 'protected', 'private')

def parseFile(file_):
    _logger.info('Entering findDefinitions %s' % repr(file_))
    
    fileToParse = File(file_)
    
    classDefinition = None
    constructorDefinitions = []
    methodDefinitions = []
    
    while fileToParse.getCurrentFileLine() is not None:
        result = _searchForClassDefinition(fileToParse)
        
        if result:
            _logger.info('Class definition found %s' % result)
            
            classDefinition = result
        else:
            result = _searchForOperationDefinition(fileToParse)
            
            if result:
                _logger.info('Operation definition found %s' % result)
                
                if isinstance(result, ConstructorDefinition):
                    constructorDefinitions.append(result)
                elif isinstance(result, MethodDefinition):
                    methodDefinitions.append(result)
                    
        fileToParse.moveToNextLine()
        
    javaParsingResult = JavaParsingResult(classDefinition, constructorDefinitions, methodDefinitions)
    
    _logger.info('Exiting findDefinition %s' % javaParsingResult)
    
    return javaParsingResult

def _searchForClassDefinition(fileToParse):
    _logger.info('Entering _searchForClassDefinition %s' % fileToParse)
    
    fileLine = fileToParse.getCurrentFileLine()
    
    match = re.search(r'(?:(?:public)|(?:private)|(?:static)|(?:protected)\s+)*(class) (\w+)', fileLine.text)
    
    output = None
    if match:
        className = match.groups()[1]
        classDefinition = ClassDefinition(className, fileLine.lineNumber, fileLine.indentationLevel + 1)
        _findEndOfDefinition(fileToParse, classDefinition)
        
        output = classDefinition
        
    _logger.info('Exiting _searchForClassDefinition %s' % output)
    
    return output

def _searchForOperationDefinition(fileToParse):
    _logger.info('Entering _searchForOperationDefinition %s' % fileToParse)
    
    fileLine = fileToParse.getCurrentFileLine()
    match = re.search(r'(\w*\<\w*\S\s*\w+\>|\w+)\s+(\w+)\((.*)\) ', fileLine.text)
    output = None
    
    if not match:
        _logger.info('Exiting _searchForOperationDefinition %s' % output)
        
        return output
        
    matchGroup = match.groups()
    
    if _isConstructorDefinition(matchGroup):
        name = matchGroup[1]
        parameters = _findParameters(matchGroup[2])
        lineNumber = fileLine.lineNumber
        
        constructorDefinition = ConstructorDefinition(name, parameters, lineNumber, fileLine.indentationLevel + 1)
        _findEndOfDefinition(fileToParse, constructorDefinition)
        
        output = constructorDefinition
    elif _isMethodDefinition(matchGroup):
        returnValue = matchGroup[0]
        name = matchGroup[1]
        parameters = _findParameters(matchGroup[2])
        lineNumber = fileLine.lineNumber
        
        methodDefinition = MethodDefinition(returnValue, name, parameters, lineNumber, fileLine.indentationLevel + 1)
        _findEndOfDefinition(fileToParse, methodDefinition)
        
        output = methodDefinition
    
    _logger.info('Exiting _searchForOperationDefinition %s' % output)
    
    return output
    
def _findEndOfDefinition(fileToParse, definition):
    _logger.info('Entering _findEndOfOperation %s %s' % (fileToParse, definition))
    
    startingLineNumber = fileToParse.getCurrentFileLine().lineNumber
    
    curlyBraceStack = []
    openBrace = '{'
    closeBrace = '}'
    
    while fileToParse.getCurrentFileLine() is not None:
        fileLine = fileToParse.getCurrentFileLine()
        
        if openBrace in fileLine.text:
            curlyBraceStack.append(openBrace)
        if closeBrace in fileLine.text:
            curlyBraceStack.pop()
            
        if isinstance(definition, MethodDefinition):
            returnStatement = _searchForReturnStatement(fileLine)
            if returnStatement:
                definition.returnStatements.append(returnStatement)
                        
        if len(curlyBraceStack) is 0:
            definition.endLineNumber = fileLine.lineNumber
            break
        
        fileToParse.moveToNextLine()
        
    if isinstance(definition, ClassDefinition):
        fileToParse.setCurrentFileLineLocation(startingLineNumber)
    
    _logger.info('Exiting _findEndOfOperation %s' % definition)
        
def _searchForReturnStatement(fileLine):
    returnStatement = 'return'
    
    if returnStatement not in fileLine.text:
        return None
    
    match = re.search(r'(return)([^;]*)', fileLine.text)
    
    if not match:
        return None
    
    matchGroup = match.groups()
    value = matchGroup[1].strip()
    
    return ReturnStatement(value, fileLine.lineNumber, fileLine.indentationLevel)
            
def _isMethodDefinition(matchGroup):
    _logger.info('Entering _isMethodDefinition %s' % repr(matchGroup))
    
    output = False

    if matchGroup[0] not in _visibilities:
        output = True
        
    _logger.info('Exiting _isMethodDefinition %s' % output)

    return output

def _isConstructorDefinition(matchGroup):
    _logger.info('Entering _isContructorDefinition %s' % repr(matchGroup))

    output = False
    
    if matchGroup[0] in _visibilities:
        output = True
    
    _logger.info('Exiting _isContructorDefinition %s'% output)

    return output

def _findParameters(text):
    _logger.info('Entering _findParameters %s' % repr(text))
                 
    parameters = []
    
    if text is []:
        _logger.info('Exiting _isContructorDefinition %s' % repr(parameters))
        
        return parameters
    
    parametersText = text.replace(',', '').split()
    
    
    for index in range(len(parametersText)):
        if index % 2 is 0:
            parameter = Parameter(None, None)
            parameter.type_ = parametersText[index]
        else:
            parameter.value = parametersText[index]
            parameters.append(parameter)
            
    _logger.info('Exiting _findParameters %s' % repr(parameters))
    
    return parameters
