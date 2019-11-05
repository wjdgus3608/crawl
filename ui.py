import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget, QLabel, QHBoxLayout, QVBoxLayout, \
    QTextEdit

class MyApp(QWidget):
    data={}
    def __init__(self):
        super().__init__()
        self.data=self.initUI()

    def initUI(self):


        self.setWindowTitle('니짐내짐 데이터 입력 프로그램')
        self.setWindowIcon(QIcon('니짐내짐.png'))
        self.resize(500, 500)
        self.center()

        keyword_lb = QLabel('검색어', self)
        id_lb = QLabel('니짐내짐 ID', self)
        pw_lb = QLabel('니짐내짐 PW', self)

        font1 = keyword_lb.font()
        font1.setPointSize(20)

        btn = QPushButton('실행', self)


        self.keyword_tx=QTextEdit()
        self.id_tx=QTextEdit()
        self.pw_tx=QTextEdit()
        btn.clicked.connect(self.submit)
        self.keyword_tx.setMaximumSize(150,30)
        self.id_tx.setMaximumSize(150,30)
        self.pw_tx.setMaximumSize(150,30)


        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(keyword_lb)
        hbox.addWidget(self.keyword_tx)
        hbox.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(id_lb)
        hbox2.addWidget(self.id_tx)
        hbox2.addStretch(1)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(pw_lb)
        hbox3.addWidget(self.pw_tx)
        hbox3.addStretch(1)

        hboxLast = QHBoxLayout()
        hboxLast.addStretch(1)
        hboxLast.addWidget(btn)
        hboxLast.addStretch(1)


        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addLayout(hbox)
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
        print(self.keyword_tx.toPlainText())
        print(self.id_tx.toPlainText())
        print(self.pw_tx.toPlainText())
        print("submit clicked!!")
        self.data['ID']=self.id_tx.toPlainText()
        self.data['PW']=self.pw_tx.toPlainText()
        self.data['KEYWORD']=self.keyword_tx.toPlainText()


def run():
    app = QApplication(sys.argv)
    ex = MyApp()
    app.exec()
    #sys.exit(app.exec_())
    return ex

