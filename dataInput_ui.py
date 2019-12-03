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
        keyword_lb = QLabel('검색어', self)
        id_lb = QLabel('니짐내짐 ID', self)
        pw_lb = QLabel('니짐내짐 PW', self)
        address_lb = QLabel('입력주소 어절', self)
        address_des = QLabel('ex)서울 영등포구 양평로 64 한경빌딩 4층 -> 4입력(추천) -> 서울 영등포구 양평로', self)

        font1 = keyword_lb.font()
        font1.setPointSize(20)

        btn = QPushButton('실행', self)


        self.keyword_tx=QTextEdit()
        self.id_tx=QTextEdit()
        self.pw_tx=QTextEdit()
        self.address_tx=QSpinBox()

        btn.clicked.connect(self.submit)
        self.keyword_tx.setMaximumSize(150,30)
        self.id_tx.setMaximumSize(150,30)
        self.pw_tx.setMaximumSize(150,30)
        self.address_tx.setRange(1,6)

#박스 설정
        hbox = self.add_box([keyword_lb,self.keyword_tx])
        hbox2 = self.add_box([id_lb,self.id_tx])
        hbox3 = self.add_box([pw_lb,self.pw_tx])
        hbox4 = self.add_box([address_lb,self.address_tx])
        hbox5 = self.add_box([address_des])


        hboxLast = QHBoxLayout()
        hboxLast.addStretch(1)
        hboxLast.addWidget(btn)
        hboxLast.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
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
        keywordtxt=self.keyword_tx.toPlainText()
        if idtxt!='' and pwtxt!='' and keywordtxt!='':
            self.data['ID']=idtxt
            self.data['PW']=pwtxt
            self.data['KEYWORD']=keywordtxt
            self.data['ADD_CNT']=self.address_tx.value()
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

