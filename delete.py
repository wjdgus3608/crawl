import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
class DataInputUI(QWidget):
    app = QApplication(sys.argv)
    data={}
    def __init__(self):
        super().__init__()

    def initUI(self):


        self.setWindowTitle('니짐내짐 데이터 입력 프로그램')
        self.setWindowIcon(QIcon('니짐내짐.png'))
        self.resize(500, 500)
        self.center()
#   라벨
        id_lb = QLabel('니짐내짐 ID', self)
        pw_lb = QLabel('니짐내짐 PW', self)

        btn = QPushButton('실행', self)

        self.id_tx=QTextEdit()
        self.pw_tx=QTextEdit()


        btn.clicked.connect(self.submit)
        self.id_tx.setMaximumSize(150,30)
        self.pw_tx.setMaximumSize(150,30)

#박스 설정
        hbox2 = self.add_box([id_lb,self.id_tx])
        hbox3 = self.add_box([pw_lb,self.pw_tx])


        hboxLast = QHBoxLayout()
        hboxLast.addStretch(1)
        hboxLast.addWidget(btn)
        hboxLast.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hboxLast)
        vbox.addStretch(3)

        self.setLayout(vbox)
        self.show()
        return self.data;

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def submit(self):
        print("submit clicked!!")
        idtxt=self.id_tx.toPlainText()
        pwtxt=self.pw_tx.toPlainText()
        if idtxt!='' and pwtxt!='':
            self.data['ID']=idtxt
            self.data['PW']=pwtxt
            self.close()
        else:
            msgBox = QMessageBox()
            msgBox.setText("내용을 모두 입력해주세요")
            msgBox.exec_()

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
        #sys.exit(app.exec_())