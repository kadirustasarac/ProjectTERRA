from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

xpos = 0
ypos = 0
WIDTH = 300
HEIGHT = 300

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setGeometry(xpos,ypos,WIDTH,HEIGHT)
        self.setWindowTitle("")
        self.initUI()
    
        self.initUI()
        self.startPlace()



    def startPlace(self):
        self.label2 = QtWidgets.QLabel(self)
    
    
    
    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("")
        self.label.move(50,50)
        self.label.setText("")

        self.b1= QtWidgets.QPushButton(self)
        self.b1.setText("")
        self.b1.clicked.connect(self.clicked)
        
    def clicked(self):
        self.label.setText("")




def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()  
    sys.exit(app.exec_())


if __name__ == "__main__":
    window()