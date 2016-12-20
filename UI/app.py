import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore


class mainScreen(QWidget):
    #
    # Calling the super to initialize the window
    #
    def __init__(self, parent=None):
        super(mainScreen, self).__init__()
        self.initMainWindow()

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
                               self.codeEditor.document().size().height() + 10);
        self.font = QFont()
        self.font.setFamily('OperatorMono-Light')
        self.font.setFixedPitch(True)
        self.font.setPointSize(12)
        self.codeEditor.setFont(self.font)
        self.codeEditor.setTabStopWidth(20)
        self.codeEditor.keyReleaseEvent = self.keyReleaseEvent
        self.cursor = self.codeEditor.textCursor()

    #Show the list when Control is entered
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.showList()
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
    def showList(self):  # Show AutoComleteList
        rect = self.codeEditor.cursorRect()
        self.clearWidget(self.suggestionList)
        self.fillList()
        self.suggestionList.move(rect.x() + 7, rect.y() + 33)
        self.suggestionList.setCurrentRow(0)
        self.suggestionList.show()

    #Clear widget elements
    def clearWidget(self, widget):
        widget.clear()

    def fillList(self):
        #Retrieve suggestion from selectCurrentWord()
        print(self.selectCurrentWord())
        for i in range(1, 30):
            self.suggestionList.addItem("QListWidget Item #" + str(i))
        numOfSuggestions = QLabel("There are " + str(self.suggestionList.count()) + "Suggestions")
        numOfSuggestions.move(50, 40)

    def itemSelect(self, item):
        self.selectCurrentWord()
        self.cursor.insertText(item.text())
        self.suggestionList.hide()

    def selectCurrentWord(self):
        self.cursor.select(QTextCursor.WordUnderCursor)
        self.codeEditor.setTextCursor(self.cursor)
        word = self.cursor.selectedText()
        return word

    def saveIntoFile(self):
        file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code-files'))
        with open(file_dir + os.sep + "current-tab.py", 'w') as codeFile:
            codeFile.write(self.codeEditor.toPlainText())


def main():
    app = QApplication(sys.argv)
    # Creating object from mainScreen
    main = mainScreen()
    sys.exit((app.exec_()))


if __name__ == "__main__":
    main()
