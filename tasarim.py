from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QImage, QPixmap
import cv2
from imageStitching import imageStitching as imgst
from procces import NDVI_procces

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1214, 822)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("QMainWindow{\n"
"background-color: \n"
"rgb(129, 143, 180);\n"
"}")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(90, 50, 1131, 761))
        self.graphicsView.setObjectName("graphicsView")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(-10, 0, 1231, 61))
        self.frame.setStyleSheet("QFrame {\n"
"    background-color:rgb(54, 48, 98)\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(1150, 0, 81, 61))
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/UI Basic outline-15.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(48, 48))
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(20, 0, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel {\n"
"    color: white;\n"
"}\n"
"")
        self.label.setObjectName("label")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(0, 50, 91, 771))
        self.frame_2.setStyleSheet("QFrame{\n"
"background-color: rgb(67, 85, 133);\n"
"}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 30, 81, 61))
        self.pushButton_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/UI Basic outline-02.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setIconSize(QtCore.QSize(48, 48))
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_3.setGeometry(QtCore.QRect(0, 100, 81, 61))
        self.pushButton_3.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/UI Basic outline-17.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setIconSize(QtCore.QSize(48, 48))
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 680, 81, 61))
        self.pushButton_4.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/UI Basic outline-73.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon3)
        self.pushButton_4.setIconSize(QtCore.QSize(48, 48))
        self.pushButton_4.setFlat(True)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_5.setGeometry(QtCore.QRect(0, 180, 81, 61))
        self.pushButton_5.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/newPrefix/UI Basic outline-107.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon4)
        self.pushButton_5.setIconSize(QtCore.QSize(48, 48))
        self.pushButton_5.setFlat(True)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_6.setGeometry(QtCore.QRect(0, 260, 81, 61))
        self.pushButton_6.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/newPrefix/UI Basic outline-118.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon5)
        self.pushButton_6.setIconSize(QtCore.QSize(48, 48))
        self.pushButton_6.setFlat(True)
        self.pushButton_6.setObjectName("pushButton_6")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(900, 60, 312, 183))
        self.calendarWidget.setObjectName("calendarWidget")
        self.frame_2.raise_()
        self.graphicsView.raise_()
        self.frame.raise_()
        self.calendarWidget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # pushButton_2 için tıklama olayını bağlama
        self.pushButton_2.clicked.connect(self.load_image)
        self.pushButton_4.clicked.connect(self.clear_image)
        self.pushButton_5.clicked.connect(self.ndvi_image)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "ProjectTERRA"))

    # Resim yüklemek için fonksiyon
    def load_image(self):
        folder_path = QFileDialog.getExistingDirectory(None, "Klasör Seç", "")
        if folder_path:
            imageList = imgst.getImages(folder_path)
            image_path = imgst.finalMethod(imageList)
        
        # Resim dosyasını seçtiriyoruz
        
        if True:
            image = cv2.cvtColor(image_path,cv2.COLOR_BGR2RGB)
            cv2.imwrite("str.jpg",image)
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)

            # QGraphicsScene ve QPixmap ile resmi QGraphicsView'e yansıtıyoruz
            scene = QGraphicsScene()
            pixmap = QPixmap(q_image)
            item = QGraphicsPixmapItem(pixmap)
            scene.addItem(item)
            self.graphicsView.setScene(scene)  # Scene'i QGraphicsView'e atıyoruz

    def clear_image(self):
        # QGraphicsView'deki sahneyi temizliyoruz
        self.graphicsView.setScene(None)
    def ndvi_image(self):
        
        image_path = "fgr.png"
        
        if image_path:
            # QGraphicsScene ve QPixmap ile resmi QGraphicsView'e yansıtıyoruz
            scene = QGraphicsScene()
            pixmap = QPixmap(image_path)
            item = QGraphicsPixmapItem(pixmap)
            scene.addItem(item)
            self.graphicsView.setScene(scene)  # Scene'i QGraphicsView'e atıyoruz
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
