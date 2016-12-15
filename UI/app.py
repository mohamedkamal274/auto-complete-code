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
        #self.move(QtGui.QApplication.desktop().availableGeometry().center() - self.frameGeometry().center())

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
        self.codeEditor = QTextEdit()
        mainLayout.addWidget(self.codeEditor, 0, 0)
        self.codeEditor.setFontFamily("Monospace")
        self.codeEditor.resize(self.codeEditor.document().size().width(), self.codeEditor.document().size().height() + 10);

        importFileButton = QPushButton("+", self)
        importFileButton.move(self.width() * 0.9, self.height() * 0.84)
        importFileButton.clicked.connect(self.showList)

        self.codeEditor.returnPressed.connect(print ("Wohooo"))

    def initAutoCompleteList(self):
        self.autoComplete = QListWidget(self)
        self.autoComplete.resize(300, 200)
        self.autoComplete.hide()
        self.autoComplete.itemClicked.connect(self.itemSelect)

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
         QMessageBox.information(self, "ListWidget", "You clicked: " + item.text())


def main():
    app = QApplication(sys.argv)
    #Creating object from mainScreen
    main = mainScreen()
    sys.exit((app.exec_()))



if __name__ == "__main__":
    main()
