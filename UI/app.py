import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
import DB
import re
import main as parser

class mainScreen(QWidget):
    #
    # Calling the super to initialize the window
    #
    dic={}
    def __init__(self, parent=None):
        super(mainScreen, self).__init__()
        self.initMainWindow()
        self.dbobject = DB.DATABASE()
        self.parserclass= parser.ClassParser()
        self.directory = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','code-files'))


    def initMainWindow(self):
        # Window sepc
        self.resize(1000, 600)
        self.setFixedSize(self.size())
        self.setWindowTitle("Auto Compelete Code")
        # Centering the screen

        # Connect CSS File
        self.styleSheet = ''
        cssFile = open('style.css', 'r')
        self.styleSheet = cssFile.read()
        cssFile.close()
        self.setStyleSheet(self.styleSheet)

        # initialize main widget
        mainLayout = QGridLayout()

        # Creating main widget
        self.setLayout(mainLayout)
        self.initTextEditor(mainLayout)
        self.initsuggestionList()
        self.show()

    def initTextEditor(self, mainLayout):
        self.codeEditor = QPlainTextEdit()
        mainLayout.addWidget(self.codeEditor, 0, 0)
        self.codeEditor.resize(self.codeEditor.document().size().width(),
                               self.codeEditor.document().size().height() + 10)
        self.font = QFont()
        self.font.setFamily('OperatorMono-Light')
        self.font.setFixedPitch(True)
        self.font.setPointSize(12)
        self.codeEditor.setFont(self.font)
        self.codeEditor.setTabStopWidth(20)
        self.codeEditor.keyReleaseEvent = self.keyReleaseEvent
        self.cursor = self.codeEditor.textCursor()

    #Show the list when Control is entered
    #for every "ctrl" parse imported modules and show list
    #for every "enter" parse previous Line
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.showList()
            importedModules = self.dbobject.getAll_modules()
            if importedModules:
                for x in importedModules:
                 self.parserclass.parse(self.directory + os.sep + x + ".py")
        elif event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            self.parse(self.selectPreviousLine())
        else:
            self.suggestionList.hide()

    def initsuggestionList(self):
        self.suggestionList = QListWidget(self)
        self.suggestionList.resize(200, 200)
        self.suggestionList.hide()
        self.suggestionList.itemClicked.connect(self.itemSelect)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(0)
        self.shadow.setColor(QColor(0, 0, 0))
        self.suggestionList.setGraphicsEffect(self.shadow)

    # suggestionListList Functions`
    #to showList determine get current line and send it to function get to get List
    def showList(self):  # Show AutoComleteList
        rect = self.codeEditor.cursorRect()
        self.clearWidget(self.suggestionList)
        arr = []
        arr = self.get(self.selectCurrentLine())
        if arr :
            self.fillList(arr)
        self.suggestionList.move(rect.x() + 7, rect.y() + 33)
        self.suggestionList.setCurrentRow(0)
        self.suggestionList.show()

    #Clear widget elements
    def clearWidget(self, widget):
        widget.clear()

    def fillList(self,item):
        #Retrieve suggestion from selectCurrentWord()
        for i in item:
            self.suggestionList.addItem(i)
        numOfSuggestions = QLabel("There are " + str(self.suggestionList.count()) + "Suggestions")
        numOfSuggestions.move(50, 40)

    def itemSelect(self, item):
        self.selectCurrentWord()
        x=item.text()
        self.dbobject.incrementCount(x)
        self.cursor.insertText(x)
        self.suggestionList.hide()

    def selectCurrentWord(self):
        self.cursor.select(QTextCursor.WordUnderCursor)
        self.codeEditor.setTextCursor(self.cursor)
        word = self.cursor.selectedText()
        return word
    def selectCurrentLine(self):
        self.cursor.movePosition(QTextCursor.StartOfBlock)
        self.cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
        line = self.cursor.selectedText()
        return line

    def selectPreviousLine(self):
        self.cursor.movePosition(QTextCursor.PreviousBlock)
        self.cursor.movePosition(QTextCursor.NextBlock, QTextCursor.KeepAnchor)
        line = self.cursor.selectedText()
        return line

    def saveIntoFile(self):
        file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code-files'))
        with open(file_dir + os.sep + "current-tab.py", 'w') as codeFile:
            codeFile.write(self.codeEditor.toPlainText())

    def get(self,line):
        arr = []
        if re.search(r'import ', line): #check if line has import
            arr = [self.parserclass.getTail(x).replace('.py', '') for x in self.parserclass.findAllPythonFiles(self.directory)]
            if re.search(r'import (.+)', line):
                modules = re.findall(r'import (.+)', line)[0].split(',')
                arr = [x for x in arr if modules[-1] in x]


        elif re.search(r'\.', line): #check if line has " . " -for-> object from class | module Data
            importedModules=self.dbobject.getAll_modules() #get all modules to check that previous dot is module or not
            MoaduleOrObject=re.findall(r'(:?(:?.+?)\s*=\s*)?(.+?)\.', line)[0][2] #get word that previous of dot to check

            if MoaduleOrObject in importedModules: #if it module
                arr=self.dbobject.getmoduleData(MoaduleOrObject) #get all module data
                word=self.selectCurrentWord() #get word to show list depend on it
                arr = [x for x in arr if word in x] #search for word in arr and append in arr

            elif MoaduleOrObject in self.dic.keys(): #if it "object" -mean->if word is in dictionary of objects
                arr=self.dbobject.selectClassData(self.dic[MoaduleOrObject][1]) #send className to get class data and append to arr
                word = self.selectCurrentWord()
                arr = [x for x in arr if word in x]
        else:
            word=self.selectCurrentWord() #else complete Modules Name
            importedModules = self.dbobject.getAll_modules()
            arr = [x for x in importedModules if word in x]
        return arr

    #to parse previous Line
    def parse(self, item):
        if re.search(r'import (.+)', item):  #check if line has import
            for x in re.findall(r'import (.+)', item)[0].replace('\u2029', '').split(','): #get all files that imported and send them to parse
                self.parserclass.parse(self.directory + os.sep + x + ".py")

        elif re.search(r'(.+?)\s*\=\s*(.+)\.(.+)', item): #check if line has declaraion object of class
            groups = re.findall(r'\s*(.+?)\s*=\s*(.+)\.(.+)',item)[0] #because it return [(groups)] and wn need tuple
            classes=self.dbobject.getmoduleClasses(groups[1]) #group 1 is ModuleName then we get all classes to check
            className = groups[2].replace('\u2029', '') #remove unicode from Name of className
            if className in classes: #check if class name is class in classes
                value=(groups[1],className) #make value of key contain (moduleName,ClassName)
                key=groups[0] #key is a object
                self.dic[key]=value #append to dictionary





def main():
    app = QApplication(sys.argv)
    # Creating object from mainScreen
    main = mainScreen()
    sys.exit((app.exec_(),main.dbobject.truncate()))


if __name__ == "__main__":
    main()