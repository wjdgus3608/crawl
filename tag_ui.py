import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import os
class TagUI(QWidget):
    app = QApplication(sys.argv)
    f = open(os.getcwd()+"/tag.txt", 'r')
    f2 = open(os.getcwd()+"/tag.txt", 'a')
    data={}
    def __init__(self):
        super().__init__()

    def initUI(self):
        line = self.f.readline()

        self.setWindowTitle('니짐내짐 데이터 입력 프로그램')
        self.setWindowIcon(QIcon('니짐내짐.png'))
        self.resize(500, 500)
        self.center()
#   라벨

        progress_lb = QLabel('태그 상태', self)
        self.txt_wid = QTextEdit()
        self.txt_wid.setMaximumSize(150, 30)
        self.tag_wid = QListWidget()
        str=line.split(',')
        print(str)
        for tmp in str:
            self.tag_wid.addItem(tmp)
        btn = QPushButton('추가', self)
        btn2 = QPushButton('삭제', self)
        btn3 = QPushButton('닫기', self)


        btn.clicked.connect(self.add)
        btn2.clicked.connect(self.delete)
        btn3.clicked.connect(self.close)

#박스 설정
        hbox = self.add_box([progress_lb])
        hbox2 = self.add_box([self.tag_wid])
        hbox3 = self.add_box([self.txt_wid,btn,btn2])
        hbox4 = self.add_box([btn3])


        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addStretch(3)

        self.setLayout(vbox)
        self.show()
        return self.data;

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def add(self):
        self.tag_wid.addItem(self.txt_wid.toPlainText())
        self.f2.write(','+self.txt_wid.toPlainText())
        self.txt_wid.clear()

    def delete(self):
        f3 = open(os.getcwd()+"/tag.txt", 'w')
        self.tag_wid.takeItem(self.tag_wid.currentRow())
        for index in range(0,self.tag_wid.count()):
            if index!=0:
                f3.write(','+self.tag_wid.item(index).text())
            else:
                f3.write(self.tag_wid.item(index).text())

    def close(self):
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
        return self.data

