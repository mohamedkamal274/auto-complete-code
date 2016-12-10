import sqlite3

#autoConnect DB
conn = sqlite3.connect('database/autoComplete.db')
cursor = conn.cursor()  #We need to use cursor to return data from selected lines(SELECT)

#DB creation Code
'''
CREATE TABLE classes (
    ID                INTEGER PRIMARY KEY AUTOINCREMENT,
    className         VARCHAR,
    moduleID          INTEGER REFERENCES Modules (ID) ON DELETE CASCADE,
    inherited_classID INTEGER REFERENCES classes (ID) ON DELETE SET NULL
                              DEFAULT NULL,
    count             INTEGER DEFAULT (0)
);

CREATE TABLE classFunction (
    ID           INTEGER PRIMARY KEY AUTOINCREMENT,
    classID              REFERENCES classes (ID) ON DELETE CASCADE,
    functionName VARCHAR,
    count        INTEGER DEFAULT (0)
);

CREATE TABLE classVariables (
    ID           INTEGER PRIMARY KEY AUTOINCREMENT,
    classID      INTEGER REFERENCES classes (ID) ON DELETE CASCADE,
    variableName VARCHAR,
    count        INTEGER DEFAULT (0),
    objectOf     INTEGER REFERENCES classes (ID) ON DELETE CASCADE,
    fromModule   INTEGER REFERENCES Modules (ID) ON DELETE CASCADE
                         DEFAULT NULL
);

CREATE TABLE moduleFunctions (
    ID           INTEGER PRIMARY KEY AUTOINCREMENT,
    moduleID     INTEGER REFERENCES Modules (ID) ON DELETE CASCADE,
    functionName VARCHAR,
    count        INTEGER DEFAULT (0)
);

CREATE TABLE Modules (
    ID         INTEGER PRIMARY KEY AUTOINCREMENT,
    moduleName STRING  UNIQUE,
    counter    INTEGER DEFAULT (0)
);

CREATE TABLE moduleVariables (
    ID             INTEGER PRIMARY KEY AUTOINCREMENT,
    moduleID       INTEGER REFERENCES Modules (ID) ON DELETE CASCADE,
    variableName   VARCHAR,
    count          INTEGER DEFAULT (0),
    objectOf_Class INTEGER REFERENCES classes (ID) ON DELETE CASCADE
                           DEFAULT NULL,
    fromModule     INTEGER REFERENCES Modules (ID) ON DELETE CASCADE
                           DEFAULT NULL
);

'''


class DATABASE():

    #add new Module in Module Table
    def addModule(self, module):
        query = "INSERT INTO 'Modules' (moduleName) VALUES ('"+module+"')"
        cursor.execute(query)
        conn.commit() #to save Database

    #get module id to be added in onther tables as FK
    def getModuleID(self, moduleName):
        query = "SELECT ID FROM 'Modules' where moduleName = '" + moduleName + "'"
        l = cursor.execute(query)
        moduleID = l.fetchone()  #fetch returns a list
        return moduleID[0]

    #get class id to be added in onther tables as FK
    def getClassID(self, className):
        query = "SELECT ID FROM 'classes' where className = '" + className + "'"
        l = cursor.execute(query)
        classID = l.fetchone()  # fetch returns a list
        return classID[0]

    #add class in classes Table
    def addClass(self, moduleName, className, parentClass):
        moduleID = self.getModuleID(moduleName)

        if parentClass != '':
            classID = self.getClassID(parentClass)
            query = "INSERT INTO classes (className,moduleID,inherited_classID) VALUES (" + "'" + className + "'" + ","\
                                                + str(moduleID) + "," + str(classID) + ")"
        else:
            query = "INSERT INTO classes (className,moduleID) VALUES (" + "'" + className + "'" + "," + str(moduleID) + ")"
        cursor.execute(query)
        conn.commit()


    #if choice = 0 then it's a normal variable
    #if choice = 1 then it's an object from the same module
    #if choice = 2 then it's and object from other module
    def addModuleVariables(self,moduleName,varName,className,fromModule,choice):
        moduleID = self.getModuleID(moduleName)
        if choice == 0:
            query = "INSERT INTO moduleVariables (moduleID,variableName) VALUES(" + str(moduleID) +\
                    ",'" + varName + "'" + ")"
        elif choice == 1:
            classID = self.getClassID(className)
            query = "INSERT INTO moduleVariables (moduleID,variableName,objectOf_Class) VALUES("+ str(moduleID) \
                    + ",'" + varName + "'," + str(classID) + ")"
        elif choice == 2:

            x = fromModule+".py" #moduleName with py to search in DB

            fromModuleID = self.getModuleID(x)

            classID = self.getClassID(className)
            query = "INSERT INTO moduleVariables (moduleID,variableName,objectOf_Class,fromModule) VALUES(" + \
            str(moduleID) + ",'" + varName + "'," + str(classID) + "," + str(fromModuleID) + ")"

        cursor.execute(query)
        conn.commit()

    #adds the function which are in the module
    def addModuleMethods(self,moduleName,methodName):
        moduleID = self.getModuleID(moduleName)
        query = "insert into moduleFunctions (moduleID,functionName) values("+ str(moduleID) + "," + "'" + methodName + "'" + ")"
        cursor.execute(query)
        conn.commit()

    #add functions which are in class
    def addfunctionsinclass(self,ClassName,methodName):
         class_id  = self.getClassID(ClassName)
         query = "insert into classFunction (classID,functionName) values ("+ str(class_id) + "," + "'" + methodName + "'" +")"
         cursor.execute(query)
         conn.commit()

    #add class normal variables
    def addClass_Normalvariable (self, ClassName,varName):
        class_id = self.getClassID(ClassName)
        query = "insert into classVariables (classID,variableName)values (" + str(class_id) + "," +"'"+ varName + "'"+ ")"
        cursor.execute(query)
        conn.commit()
    #add class variables which are object from classes in the same module
    def addClass_object_variable(self, ClassName, varName,class_object):
        class_id = self.getClassID(ClassName)
        classObjectID = self.getClassID(class_object)
        query = "insert into classVariables (classID,variableName,objectOf)values (" + str(class_id) + "," + "'" + varName + "'" + "," + str(classObjectID) +")"
        cursor.execute(query)
        conn.commit()

    #add class vaiables which are objects from another classes in another modules
    def addClass_object_othermodule(self, ClassName, varName, class_object ,class_module):
        v = class_module+".py"
        class_id = self.getClassID(ClassName)
        classObjectID= self.getClassID(class_object)
        moduleID = self.getModuleID(class_module+".py")
        query = "insert into classVariables (classID,variableName,objectOf,fromModule )values (" + str(  class_id) + "," + "'" + varName + "'" + "," + str(classObjectID) + "," + str(moduleID) + ")"
        cursor.execute(query)
        conn.commit()

    #get class data and get parent class data if he inherts
    def selectClassData(self, className):
        classID = self.getClassID(className)
        list = []
        query = "SELECT variableName FROM classVariables where classID=" + str(classID)
        record = cursor.execute(query)
        for x in record:
            list.append(x[0])
        query = "SELECT functionName FROM classFunction where classID=" + str(classID)
        record = cursor.execute(query)
        for x in record:
            list.append(x[0])

        #get PARENT DATA
        query = "SELECT inherited_classID FROM classes WHERE className =" + "'" + className + "'"
        record = cursor.execute(query)
        parentClass = record.fetchone()
        if parentClass != None:
            query = "SELECT variableName FROM classVariables where classID=" + str(parentClass[0])
            record = cursor.execute(query)
            for x in record:
                list.append(x[0])
            query = "SELECT functionName FROM classFunction where classID=" + str(parentClass[0])
            record = cursor.execute(query)
            for x in record:
                list.append(x[0])

        return list


