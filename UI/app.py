import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class mainScreen(QWidget):
    #
    #Calling the super to initialize the window
    #
    def __init__(self, parent = None):
        super(mainScreen, self).__init__()
        self.initMainWindow()

    def initMainWindow(self):
        #Window sepc
        self.resize(1000,600)
        self.setFixedSize(self.size())
        self.setWindowTitle("Auto Compelete Code")
        #Centering the screen

        #Connect CSS File
        self.styleSheet = ''
        cssFile = open('style.css', 'r')
        self.styleSheet = cssFile.read()
        cssFile.close()
        self.setStyleSheet(self.styleSheet)

        #initialize main widget
        mainLayout = QGridLayout()

        #Creating main widget
        self.setLayout(mainLayout)
        self.initTextEditor(mainLayout)
        self.initAutoCompleteList()
        self.show()

    def initTextEditor(self, mainLayout):
        self.codeEditor = QPlainTextEdit()
        mainLayout.addWidget(self.codeEditor, 0, 0)
        self.codeEditor.resize(self.codeEditor.document().size().width(), self.codeEditor.document().size().height() + 10);
        self.font = QFont()
        self.font.setFamily('OperatorMono-Light')
        self.font.setFixedPitch(True)
        self.font.setPointSize(12)
        #self.highlighter = Highlighter(self.codeEditor.document())

        self.codeEditor.setFont(self.font)
        self.codeEditor.setTabStopWidth(20)


        importFileButton = QPushButton("+", self)
        importFileButton.move(self.width() * 0.9, self.height() * 0.84)
        importFileButton.clicked.connect(self.currentLocation)

    def initAutoCompleteList(self):
        self.autoComplete = QListWidget(self)
        self.autoComplete.resize(200, 200)
        self.autoComplete.hide()
        self.autoComplete.itemClicked.connect(self.itemSelect)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(0)
        self.shadow.setColor(QColor(0,0,0))
        self.autoComplete.setGraphicsEffect(self.shadow)

    # AutoCompleteList Functions

    def showList(self):             # Show AutoComleteList
        rect = self.codeEditor.cursorRect()
        self.clearWidget(self.autoComplete)
        self.fillList()
        self.autoComplete.move(rect.x() + 7, rect.y() + 33)
        self.autoComplete.setCurrentRow(0)
        self.autoComplete.show()


    def clearWidget(self, widget):
        widget.clear()

    def fillList(self):
        # That fill is for only testing , you can update it
        for i in range(1, 30):
             self.autoComplete.addItem("QListWidget Item #" + str(i))
        numOfSuggestions = QLabel("There are "+str(self.autoComplete.count())+"Suggestions")
        numOfSuggestions.move(50,40)

    def itemSelect(self, item):
         print("ListWidget", "You clicked: " + item.text())

    def saveIntoFile(self):
        file_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'code-files'))
        with open(file_dir + os.sep + "current-tab.py", 'w') as codeFile:
            codeFile.write(self.codeEditor.toPlainText())

    def currentLocation(self):
        cursor = QTextCursor()
        cursor = self.codeEditor.textCursor();
        y = cursor.blockNumber() + 1
        x = cursor.columnNumber() + 1
        print (x, y)
        #cursor.insertText("TEST")

def main():
    app = QApplication(sys.argv)
    #Creating object from mainScreen
    main = mainScreen()
    sys.exit((app.exec_()))

if __name__ == "__main__":
    main()
