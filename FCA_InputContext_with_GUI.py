import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QGridLayout, QPushButton, QFileDialog, QLabel, QTextBrowser


class FCAInputContextGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.num = 0
        self.setWindowTitle('FCA InputContext GUI')
        self.resize(800, 600)
        self.center()

        self.data = 0

        self.Lgrid = QGridLayout()
        self.setLayout(self.Lgrid)

        self.label1 = QLabel('FCA Input Context', self)
        self.label2 = QLabel('', self)
        self.label3 = QLabel('[실행결과]', self)

        self.Lgrid.addWidget(self.label1, 0, 0)

        self.addbutton1 = QPushButton('Context 입력(Open CSV File)', self)
        self.Lgrid.addWidget(self.addbutton1, 1, 0)
        self.addbutton1.clicked.connect(self.csv_open)

        self.addbutton2 = QPushButton('실행', self)
        self.Lgrid.addWidget(self.addbutton2, 1, 1)
        self.addbutton2.clicked.connect(lambda: self.InputContext(self.label2.text()))

        self.Lgrid.addWidget(self.label2, 2, 0)
        self.Lgrid.addWidget(self.label3, 3, 0)

        self.resultsh = QTextBrowser()
        self.Lgrid.addWidget(self.resultsh, 4, 0)

        self.show()

    def csv_open(self):
        FileOpen = QFileDialog.getOpenFileName(self, 'Open file', './', 'csv(*.csv)')
        self.label2.setText(FileOpen[0])

    def InputContext(self, FilePath):
        self.data = pd.read_csv(FilePath)
        G = set(self.data.index)
        M = set(self.data.columns)
        I = set()

        # Process : Formal Context를 읽어들여서 "적절한 Data구조 K"에 저장". formal context K:=(G, M, I)
        for g in G:
            for m in M:
                if self.data[m][g] in ['x', 'X']:
                    I.add((g, m))

        K = [G, M, I]
        self.resultsh.append(str(K))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FCAInputContextGUI()
    sys.exit(app.exec_())