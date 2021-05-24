# FCA InputContext with gui
# 2018210032 김태영
# 2021.05.23

import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QGridLayout, QPushButton, QFileDialog, QLabel, QTextBrowser

class FCAInputContextGUI(QWidget):

    def __init__(self):
        super().__init__()

        # 기본 창 설정
        self.setWindowTitle('FCA InputContext GUI')
        self.resize(800, 600)
        self.center()

        # 그리드 레이아웃을 사용한 위젯 배치 및 설정
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        # 라벨 생성 및 설정
        self.titleL = QLabel('FCA Input Context', self)  # 타이틀 라벨
        self.filePathL = QLabel('', self)  # 선택한 파일 경로를 보여줄 라벨
        self.resultTitleL = QLabel('[실행결과]', self)  # 실행결과 타이틀 라벨

        self.grid.addWidget(self.titleL, 0, 0)
        self.grid.addWidget(self.filePathL, 2, 0)
        self.grid.addWidget(self.resultTitleL, 3, 0)

        # 파일 오픈 버튼 생성 및 설정
        self.fileOpenB = QPushButton('Context 입력(Open CSV File)', self)
        self.grid.addWidget(self.fileOpenB, 1, 0)
        self.fileOpenB.clicked.connect(self.csv_open)

        # 실행 버튼 생성 및 설정
        self.InputContextB = QPushButton('실행', self)
        self.grid.addWidget(self.InputContextB, 1, 1)
        self.InputContextB.clicked.connect(lambda: self.InputContext(self.filePathL.text()))

        # 실행 결과 출력 화면 생성 및 설정
        self.resultS = QTextBrowser()
        self.grid.addWidget(self.resultS, 4, 0)

        self.show()

    # 창을 화면 가운데에 띄우는 함수
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # csv file open 및 filePath 출력 함수
    def csv_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './', 'csv(*.csv)')
        self.filePathL.setText(fname[0])

    # Input Context 실행 함수
    def InputContext(self, fPath):

        data = pd.read_csv(fPath)

        # G : 객체들의 집합, M : 속성들의 집합, I : 객체와 속성 사이의 관계 집합 (I ⊆ G × M)
        G = set(data.index)
        M = set(data.columns)
        I = set()

        # Process : Formal Context를 읽어들여서 "적절한 Data구조 K"에 저장". formal context K:=(G, M, I)
        for g in G:
            for m in M:
                if data[m][g] in ['x', 'X']:
                    I.add((g, m))

        K = [G, M, I]
        self.resultS.append(str(K))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FCAInputContextGUI()
    sys.exit(app.exec_())
