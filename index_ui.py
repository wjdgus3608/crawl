import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import tag_ui,dataInput_ui
class IndexUI(QWidget):
    app = QApplication(sys.argv)
    mode=-1
    def __init__(self):
        super().__init__()

    def initUI(self):


        self.setWindowTitle('니짐내짐 데이터 입력 프로그램')
        self.setWindowIcon(QIcon('니짐내짐.png'))
        self.resize(500, 500)
        self.center()
#   라벨


        btn1 = QPushButton('데이터 입력', self)
        btn2 = QPushButton('종목 추가/삭제', self)
        btn1.clicked.connect(self.onClick1)
        btn2.clicked.connect(self.onClick2)

#박스 설정
        hbox = self.add_box([btn1,btn2])
        self.setLayout(hbox)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def onClick1(self):
        print("onClick1 clicked!!")
        self.mode = 1;
        self.close()
    def onClick2(self):
        print("onClick2 clicked!!")
        self.mode = 2;
        self.close()
    def add_box(self,wid):
        hbox=QHBoxLayout()
        hbox.addStretch(1)
        for tmp in wid:
            hbox.addWidget(tmp)
        hbox.addStretch(1)
        return hbox
    def run(self):
        self.initUI()
        self.show()
        self.app.exec_()
        #sys.exit(self.app.exec_())
        return self.mode

