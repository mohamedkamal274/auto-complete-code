import re
import os
from os.path import join

class ClassParser(object):
   class_expr = re.compile(r'class (.+?)(?:\((.+?)\))?:')
   python_file_expr = re.compile(r'^\w+[.]py$')
   methodre = re.compile(r'def (.+?)(?:\((.*?)\))?\s*:')
   variable = re.compile(r'\s*(.+)\s*=\s*(.+)')
   objectre = re.compile(r'\s*(.+)=(.+)\.(.+)')
   indent = "   "

   def findAllClasses(self, python_file):
      #Read in a python file and return all the class names

      with open(python_file) as infile:
         everything = infile.read()
         class_names = ClassParser.class_expr.findall(everything)
         self.addNameeClasses(python_file,class_names)
         return class_names

   def findAllPythonFiles(self, directory):
      #Find all the python files starting from a top level directory

      python_files = []
      for root, dirs, files in os.walk(directory):
         for file in files:
            if ClassParser.python_file_expr.match(file):
               python_files.append(join(root,file))
      self.addNameeModule(python_files)
      return python_files

   def parse(self, directory):
      """ Parse the directory and spit out a csv file
      """
      python_files = self.findAllPythonFiles(directory)
      for file in python_files:
          classes = self.findAllClasses(file)
          self.method_modules(file)
          self.variable_moudles(file)
          for classname in classes:
              self.findClassemethod(classname[0],file)
              self.findClassevariables(classname[0],file)

   def findClassemethod(self, classname , python_file):
       #Read in a python file and return all the class methodes

       classnamere = re.compile(r'class '+classname+'(?:\((.+?)\))?:')
       methods = []
       with open(python_file) as infile:
            flag = True
            for line in infile.readlines():
                if flag == False:
                    if self.indent in line:
                        methods += self.methodre.findall(line)
                    else:
                        break
                if flag == True:
                    class_name = classnamere.findall(line)
                    if class_name:
                        flag = False
       #print( python_file ,' ',classname , ' : ' ,methods)
       self.addmethodClass(python_file,classname,methods)

   def findClassevariables(self, classname, python_file):
       varibles = []
       classnamere = re.compile(r'class ' + classname + '(?:\((.+?)\))?:')
       with open(python_file) as infile:
           flag = True
           for line in infile:
               if flag == False:
                   if self.indent in line:
                       if not 'def' in line and not 'class' in line:
                           if '.' in line:
                            varibles += self.objectre.findall(line)
                           else:
                               varibles += self.variable.findall(line)
                   else:
                       break
               if flag == True:
                   class_name = classnamere.findall(line)
                   if class_name:
                       flag = False
       #print(classname, ' : ', varibles)
       self.addvariableClass(python_file,classname,varibles)

   def method_modules(self,python_file):
        methods = []
        with open(python_file) as infile:
           for line in infile:
               if not self.indent in line:
                   methods += self.methodre.findall(line)
        #print(python_file ,' method for modules' , methods)
        self.addmethodModule(python_file,methods)

   def variable_moudles(self, python_file):
       varibles = []
       with open(python_file) as infile:
           for line in infile:
               if not self.indent in line and not 'def' in line and not 'class' in line:
                   if '.' in line:
                       varibles += self.objectre.findall(line)
                   else:
                       varibles += self.variable.findall(line)
       #print('varibles for modules', varibles)
       self.addvariableModule(python_file,varibles)





   def getTail(self,python_file):
       head, tail = os.path.split(python_file)
       return tail

   def addNameeModule(self,modulename):

       for module in modulename:
        tail=self.getTail(module)
        print (tail)


   def addNameeClasses(self,python_file,classnameS):
       tail = self.getTail(python_file)

       for classname in classnameS:
           print ('module:', tail, 'className:', classname[0],'inheritedClass:',classname[1])


   def addmethodModule(self, python_file,methods):
       tail = self.getTail(python_file)
       for method in methods:
        print ('module:', tail,'function: ',method[0],'parameter:',method[1])


   def addvariableModule(self, python_file,varibles):
       tail = self.getTail(python_file)
       module_class=[]
       classes=self.findAllClasses(python_file);
       for classname in classes:
         module_class.append(classname[0])

       #print ("calsses : --> ",module_class)

       for variable in varibles:
           if(len(variable)>2):
               print ('module:', tail,'object:',variable[0],'moduleOfobject:',variable[1],'class:',variable[2])
           else:
                if variable[1] in module_class :#can check if object in classnames or Not if found then 'object:'=variable[0]& 'class:',variable[1]
                 print ('module:', tail,'object:',variable[0],'Class:',variable[1])
                else:
                    print ('module:', tail, 'object:', variable[0], 'variable:', variable[1])


   def addvariableClass(self,python_file,classname,varibles):
       tail = self.getTail(python_file)
       for variable in varibles:
           if (len(variable) > 2):
               print ('module:', tail,'className:',classname, 'object:', variable[0], 'moduleOfobject:', variable[1], 'class:', variable[2])
           else:  # can check if object in classnames or Not if found then 'object:'=variable[0]& 'class:',variable[1]
               print ('module:', tail,'className:',classname, 'object:', variable[0],'ClassORvariable:',variable[1])

   def addmethodClass(self, python_file,classname,methods):
       tail = self.getTail(python_file)
       for method in methods:
           print ('module:', tail, 'className:',classname, 'function:', method[0], 'parameter:', method[1])


if __name__=="__main__":
   parser = ClassParser()
   dir_path = os.path.dirname(os.path.realpath(__file__)) + os.sep +"code-files"
   parser.parse(dir_path)
