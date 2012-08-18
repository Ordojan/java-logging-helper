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

def findDefinitions(file_):
    pass    