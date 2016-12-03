import re
import os
from os.path import join

class ClassParser(object):
   class_expr = re.compile(r'class (.+?)(?:\((.+?)\))?:')
   python_file_expr = re.compile(r'^\w+[.]py$')
   methodre = re.compile(r'def (.+?)(?:\((.+?)\))?:')
   variable = re.compile(r'(.+?)(?:\((.+?)\))?=')
   indent = "   "

   def findAllClasses(self, python_file):
      #Read in a python file and return all the class names

      with open(python_file) as infile:
         everything = infile.read()
         class_names = ClassParser.class_expr.findall(everything)
         return class_names

   def findAllPythonFiles(self, directory):
      #Find all the python files starting from a top level directory

      python_files = []
      for root, dirs, files in os.walk(directory):
         for file in files:
            if ClassParser.python_file_expr.match(file):
               python_files.append(join(root,file))
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
       print( python_file ,' ',classname , ' : ' ,methods)

   def findClassevariables(self, classname, python_file):
       varibles = []
       classnamere = re.compile(r'class ' + classname + '(?:\((.+?)\))?:')
       with open(python_file) as infile:
           flag = True
           for line in infile:
               if flag == False:
                   if self.indent in line:
                       if not 'def' in line and not 'class' in line:
                           varibles += self.variable.findall(line)
                   else:
                       break
               if flag == True:
                   class_name = classnamere.findall(line)
                   if class_name:
                       flag = False
       varibles = [string[0].replace(" ","") for string in varibles]
       print(classname, ' : ', varibles)

   def method_modules(self,python_file):
        methods = []
        with open(python_file) as infile:
           for line in infile:
               if not self.indent in line:
                   methods += self.methodre.findall(line)
        print(python_file ,' method for modules' , methods)

   def variable_moudles(self, python_file):
       varibles = []
       with open(python_file) as infile:
           for line in infile:
               if not self.indent in line and not 'def' in line and not 'class' in line:
                   varibles += self.variable.findall(line)
       varibles = [string[0].replace(" ","") for string in varibles]
       print('varibles for modules', varibles)


if __name__=="__main__":
   parser = ClassParser()
   dir_path = os.path.dirname(os.path.realpath(__file__)) + os.sep +"code-files"
   parser.parse(dir_path)
