import os
import sys
from PyQt4 import QtGui, QtCore
from PyQt4 import Qt

class mainScreen(QtGui.QWidget):
    def __init__(self, parent = None):
        super(mainScreen, self).__init__()
        self.initUI()

    def initUI(self):
        #Window sepc
        self.setGeometry(0,0,1000,600)
        self.setWindowTitle("Auto Compelete Code")
        #Centering the screen
        self.move(QtGui.QApplication.desktop().availableGeometry().center() - self.frameGeometry().center())

        self.show()

def main():
    app = QtGui.QApplication(sys.argv);
    main = mainScreen()
    sys.exit((app.exec_()))

if __name__ == "__main__":
    main()
