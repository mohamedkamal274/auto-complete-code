import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

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
        self.show()

    def initTextEditor(self, mainLayout):
        codeEditor = QTextEdit("TEST")
        mainLayout.addWidget(codeEditor, 0, 0)
        codeEditor.setFontFamily("Monospace")
        #font = QFont("OperatorMono-Light", 10)
        #codeEditor.setFont(font)
        #Resize the textfield to fit the screen
        codeEditor.resize(codeEditor.document().size().width(), codeEditor.document().size().height() + 10);

        importFileButton = QPushButton("+", self)
        importFileButton.move(self.width() * 0.9, self.height() * 0.84)


def main():
    app = QApplication(sys.argv)
    #Creating object from mainScreen
    main = mainScreen()
    sys.exit((app.exec_()))

if __name__ == "__main__":
    main()
