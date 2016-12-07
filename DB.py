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
        print(query)
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
