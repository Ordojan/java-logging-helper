import logging, settings, re

class Definition(object):
    def __init__(self, lineNumber, name):
        self.lineNumber = lineNumber
        self.name = name
        
    def __repr__(self):
        return 'Operation(lineNumber = {0}, name = {1})'.format(self.lineNumber, self.name)
    
class ClassDefinition(Definition):
    def __init__(self, lineNumber, name):
        super(ClassDefinition, self).__init__(lineNumber, name)
        
    def __repr__(self):
        return 'ClassDefinition(lineNumber = {0}, name = {1})'.format(self.lineNumber, self.name)
        
class MethodDefinition(Definition):
    def __init__(self, lineNumber, name, returnValue, parameters):
        super(MethodDefinition, self).__init__(lineNumber, name)
        self.returnValue = returnValue
        self.parameters = parameters
        
    def __repr__(self):
        return 'MethodDefinition(lineNumber = {0}, name = {1}, returnValue = {2}, parameters = {3})'.format(self.lineNumber, self.name, self.returnValue, self.parameters) 

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
        return 'FileLine(text = {0}, lineNumber = {1})'.format(self.text, self.lineNumber) 
    
logger = logging.getLogger(settings.LOGGER_NAME) 
    
def findDefinitions(file_):
    logger.info('Entering findDefinitions {0}'.format(repr(file_)))
    
    fileLines = file_.readlines()
    
    for line in fileLines:
        lineNumber = fileLines.index(line) + 1
        fileLine = FileLine(line, lineNumber)
        
        result = searchForClassDefinition(fileLine)
        
        if result:
            logger.info('Class definition found {0}'.format(repr(result)))
        
def searchForClassDefinition(fileLine):
    logger.info('Entering searchForClassDefinition {0}'.format(repr(fileLine)))
    
    match = re.search('(?:(?:public)|(?:private)|(?:static)|(?:protected)\s+)*(class) (\w+)', fileLine.text)
    
    output = None
    if match:
        className = match.groups()[1]
        output = ClassDefinition(fileLine.lineNumber, className)
        
    logger.info('Exiting searchForClassDefinition {0}'.format(output))
    
    return output
    
