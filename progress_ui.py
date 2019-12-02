import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
import work
class ProgressUI(QWidget):

    data={}
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):


        self.setWindowTitle('니짐내짐 데이터 입력 프로그램')
        self.setWindowIcon(QIcon('니짐내짐.png'))
        self.resize(500, 500)
        self.center()
#   라벨
        log_lb = QLabel('Logs', self)
        progress_lb = QLabel('진행률', self)
        self.progress_value_lb=QLabel('0%', self)

        self.btn = QPushButton('취소', self)

        self.log_wid=QListWidget()
        self.progress_wid=QProgressBar()

        self.btn.clicked.connect(self.submit)

#박스 설정
        hbox7 = self.add_box([log_lb,self.log_wid])
        hbox8 = self.add_box([progress_lb,self.progress_wid,self.progress_value_lb])


        hboxLast = QHBoxLayout()
        hboxLast.addStretch(1)
        hboxLast.addWidget(self.btn)
        hboxLast.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addLayout(hbox8)
        vbox.addLayout(hbox7)
        vbox.addLayout(hboxLast)
        vbox.addStretch(3)

        self.setLayout(vbox)
        self.show()
        th1 = work.Work(self)

        th1.start()
        th1.countChanged.connect(self.onCountChanged)
        th1.logChanged.connect(self.onLogChanged)
        th1.insertChanged.connect(self.onInsertChanged)
        return self.data;

    def onCountChanged(self, value):
        self.progress_wid.setValue(value)
        self.progress_value_lb.setText(str(value)+'%')
        if(value==100):
            self.btn.setText("완료")
    def onLogChanged(self, log):
        self.log_wid.addItem(log)

    def onInsertChanged(self, inserted):
        for index in range(0,self.log_wid.count()):
            self.log_wid.addItem(self.log_wid.item(index).text()+inserted)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def submit(self):
        self.close()

    def add_box(self,wid):
        hbox=QHBoxLayout()
        hbox.addStretch(1)
        for tmp in wid:
            hbox.addWidget(tmp)
        hbox.addStretch(1)
        return hbox



