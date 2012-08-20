import logging, settings, re

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
        self.name = name
        
    def __repr__(self):
        return 'Definition(name = {0}, lineNumber = {1})'.format(self.name, self.lineNumber)
    
class ClassDefinition(Definition):
    def __init__(self, name, lineNumber ):
        super(ClassDefinition, self).__init__(name, lineNumber)
        
    def __repr__(self):
        return 'ClassDefinition(name = {0}, lineNumber = {1})'.format(self.name, self.lineNumber)
        
class MethodDefinition(Definition):
    def __init__(self, returnValue, name, parameters, lineNumber):
        super(MethodDefinition, self).__init__(name, lineNumber)
        self.returnValue = returnValue
        self.parameters = parameters
        
    def __repr__(self):
        return 'MethodDefinition(returnValue = {0}, name = {1}, parameters = {2}, lineNumber = {3})'.format(self.returnValue, self.name, self.parameters, self.lineNumber) 

class ConstructorDefinition(Definition):
    def __init__(self,  name, parameters, lineNumber):
        super(ConstructorDefinition, self).__init__(name, lineNumber)
        self.parameters = parameters
        
    def __repr__(self):
        return 'ConstructorDefinition(name = {0}, parameters = {1}, lineNumber = {2})'.format(self.name, self.parameters, self.lineNumber) 
    
class Parameter(object):
    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value
        
    def __repr__(self):
        return 'Parameter(type_ = {0}, value = {1})'.format(self.type_, self.value) 

class FileLine(object):
    def __init__(self, text, lineNumber):
        self.text = text
        self.lineNumber = lineNumber
       
    def __repr__(self):
        text = self.text.strip('\n')
        return 'FileLine(text = {0}, lineNumber = {1})'.format(text, self.lineNumber)          

def findDefinitions(file_):
    _logger.info('Entering findDefinitions {0}'.format(repr(file_)))
    
    fileLines = file_.readlines()
    
    classDefinition = None
    constructorDefinitions = []
    methodDefinitions = []
    
    for line in fileLines:
        lineNumber = fileLines.index(line) + 1
        fileLine = FileLine(line, lineNumber)
        
        result = _searchForClassDefinition(fileLine)
        
        if result:
            _logger.info('Class definition found {0}'.format(result))
            
            classDefinition = result
        else:
            result = _searchForOperationDefinition(fileLine)
            
            if result:
                _logger.info('Operation definition found {0}'.format(result))
                
                if isinstance(result, ConstructorDefinition):
                    constructorDefinitions.append(result)
                elif isinstance(result, MethodDefinition):
                    methodDefinitions.append(result)
        
    javaParsingResult = JavaParsingResult(classDefinition, constructorDefinitions, methodDefinitions)
    
    _logger.info('Exiting findDefinitions {0}'.format(javaParsingResult))
    
    return javaParsingResult

def _searchForClassDefinition(fileLine):
    _logger.info('Entering _searchForClassDefinition {0}'.format(repr(fileLine)))
    
    match = re.search(r'(?:(?:public)|(?:private)|(?:static)|(?:protected)\s+)*(class) (\w+)', fileLine.text)
    
    output = None
    if match:
        className = match.groups()[1]
        classDefinition = ClassDefinition(className, fileLine.lineNumber)
        output = classDefinition
        
    _logger.info('Exiting _searchForClassDefinition {0}'.format(output))
    
    return output

def _searchForOperationDefinition(fileLine):
    _logger.info('Entering _searchForOperationDefinition {0}'.format(repr(fileLine)))
    
    match = re.search(r'(\w+)\W(\w+)\((.*)\)', fileLine.text)
    output = None
    
    if not match:
        _logger.info('Exiting _searchForOperationDefinition {0}'.format(repr(output)))
        
        return output
        
    matchGroup = match.groups()
    
    # is constructor definition
    
    
    if _isConstructorDefinition(matchGroup):
        name = matchGroup[1]
        parameters = _findParameters(matchGroup[2])
        lineNumber = fileLine.lineNumber
        
        constructorDefinition = ConstructorDefinition(name, parameters, lineNumber)
        output = constructorDefinition
    elif _isMethodDefinition(matchGroup):
        returnValue = matchGroup[0]
        name = matchGroup[1]
        parameters = _findParameters(matchGroup[2])
        lineNumber = fileLine.lineNumber
        
        methodDefinition = MethodDefinition(returnValue, name, parameters, lineNumber)
        output = methodDefinition
    
    _logger.info('Exiting _searchForOperationDefinition {0}'.format(output))
    
    return output
    
def _isMethodDefinition(matchGroup):
    _logger.info('Entering _isMethodDefinition {0}'.format(matchGroup))
    
    output = False
    visabilities = ['public', 'protected', 'private']
    
    if matchGroup[0] not in visabilities:
        output = True
        
    _logger.info('Exiting _isMethodDefinition {0}'.format(output))

    return output

def _isConstructorDefinition(matchGroup):
    _logger.info('Entering _isContructorDefinition {0}'.format(matchGroup))

    output = False
    visabilities = ['public', 'protected', 'private']
    
    if matchGroup[0] in visabilities:
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