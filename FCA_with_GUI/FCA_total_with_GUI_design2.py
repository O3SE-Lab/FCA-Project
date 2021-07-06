# FCA with GUI
# 2018210032 김태영

# [진행 완료 사항]
# Context 입력(open csv file) 부분을 탭 밖(탭 윗부분)에 배치
# 이전 버전에서 변경 사항 : Context 입력(open csv file) 부분을 탭 밖(탭 윗부분)에 배치하여 Context 입력은 한번만 해도 되도록 배치

# [진행 해야 할 사항]
# - 각 tab 내 GUI 좀 더 괜찮은 구조 있으면 수정
# - 일부 변수명 의미있게 수정
# - 탭 밖(탭 윗부분)에서 받아온 FliePath를 각 클래스가 전달(?)받을 수 있게
# - CA CO def 구현 부분 문제 해결
# - Formal Concept GUI & 구현

# 만들 때 참고한 사이트 : https://wikidocs.net/book/2165

import pandas as pd
import sys
from PyQt5.QtWidgets import *

# Widget : 화면에 표시할 수 있는 것을 목적으로 함. ex) 버튼, 사용자 입력 등
# Dialog : MainWindow의 특별한 종류. 대화상자가 항상 별도의 창에 표시되는 최상위 위젯(다른 위젯에 넣을 수 없음)
# MainWindow : 메뉴바, 스테이터스바 등 미리 설정되어있는 최상위 위젯

# Main
class FCAwithGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        ICtitleL = QLabel('[ Context 입력 ]') # context 입력 타이틀 라벨
        ICfptitleL = QLabel('  선택 파일(*.csv) : ', self)  # 선택 파일 타이틀 라벨
        ICfilePathL = QLabel('', self)  # 선택한 파일 경로를 보여줄 라벨

        ICfileOpenB = QPushButton('Context 입력(Open CSV File)', self) # context 입력 버튼(csv 파일 open 버튼)
        ICfileOpenB.clicked.connect(self.csv_open) # 버튼 클릭 시 csv_open()실행

        # 탭 생성
        tabs = QTabWidget()
        tabs.addTab(ICTab(), 'InputContext')
        tabs.addTab(CACOTab(), 'CACO')
        tabs.addTab(FCTab(), 'FormalConcept')

        hbox1 = QHBoxLayout()
        hbox1.addWidget(ICfptitleL)
        hbox1.addWidget(ICfilePathL)

        # 박스 레이아웃을 이용해 배치
        vbox = QVBoxLayout()
        vbox.addWidget(ICtitleL)
        vbox.addLayout(hbox1)
        vbox.addWidget(ICfileOpenB)
        vbox.addWidget(tabs)
        self.setLayout(vbox)

        # 기본 창 설정
        self.setWindowTitle('FCA with GUI')
        self.resize(1000, 800)
        self.center()
        self.show()

    # 창을 화면 가운데에 띄우는 함수
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def csv_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './', 'csv(*.csv)')
        self.ICfilePathL.setText(fname[0])

# InputContext Tab
class ICTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # InputContext - 라벨 생성
        ICresultTitleL = QLabel('[ Input Context 실행결과 ]', self)  # IC 실행결과 타이틀 라벨

        # InputContext - 실행 결과 출력할 텍스트 브라우저 생성
        ICtb = QTextBrowser()

        # InputContext - 파일 오픈 및 실행, CLEAR 버튼 생성
        ICexcuteB = QPushButton('실행', self)
        clearB = QPushButton('CLEAR', self)

        # 박스레이아웃을 사용한 배치
        hbox2 = QHBoxLayout()
        hbox2.addWidget(ICexcuteB)
        hbox2.addWidget(clearB)

        vbox = QVBoxLayout()
        vbox.addWidget(ICresultTitleL)
        vbox.addWidget(ICtb)
        vbox.addLayout(hbox2)
        self.setLayout(vbox)

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

        self.ICtb.append(" G ".center(80, '-'))
        self.ICtb.append(str(G))
        self.ICtb.append(" M ".center(80, '-'))
        self.ICtb.append(str(M))
        self.ICtb.append(" I ".center(80, '-'))
        self.ICtb.append(str(I))
        self.ICtb.append(" K ".center(80, '-'))
        self.ICtb.append(str(K))

        return K

    def csv_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './', 'csv(*.csv)')
        self.ICfilePathL.setText(fname[0])

    # ICtextBrowser clear 함수
    def IC_clear_text(self):
        self.ICtb.clear()

# CA CO Tab
class CACOTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # CACO - 라벨 생성 및 설정
        CAtitleL = QLabel('[CA]', self)  # CA 타이틀 라벨
        CAresultTitleL = QLabel('[CA 실행결과]', self)  # CA 실행결과 타이틀 라벨
        jtext2L = QLabel('-' * 118)
        COtitleL = QLabel('[CO]', self)  # CO 타이틀 라벨
        COresultTitleL = QLabel('[CO 실행결과]', self)  # CO 실행결과 타이틀 라벨

        # CACO - 텍스트에디터(입력받는부분) 생성
        CAte = QTextEdit()
        COte = QTextEdit()

        # CACO - 버튼
        CAexcuteB = QPushButton('실행', self)
        CAclearB = QPushButton('CLEAR', self)
        COexcuteB = QPushButton('실행', self)
        COclearB = QPushButton('CLEAR', self)

        # CACO - 텍스트브라우저(실행 결과 출력) 생성
        CAtb = QTextBrowser()
        COtb = QTextBrowser()

        # 변수명 수정 필요
        hbox3 = QHBoxLayout()
        hbox3.addWidget(CAexcuteB)
        hbox3.addWidget(CAclearB)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(COexcuteB)
        hbox4.addWidget(COclearB)

        hbox5 = QHBoxLayout()
        hbox5.addWidget(CAtitleL)
        hbox5.addWidget(CAresultTitleL)

        hbox6 = QHBoxLayout()
        hbox6.addWidget(CAte)
        hbox6.addWidget(CAtb)

        hbox7 = QHBoxLayout()
        hbox7.addWidget(COtitleL)
        hbox7.addWidget(COresultTitleL)

        hbox8 = QHBoxLayout()
        hbox8.addWidget(COte)
        hbox8.addWidget(COtb)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
        vbox.addLayout(hbox3)
        vbox.addWidget(jtext2L)
        vbox.addLayout(hbox7)
        vbox.addLayout(hbox8)
        vbox.addLayout(hbox4)
        self.setLayout(vbox)

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

        self.ICtb.append(" G ".center(80, '-'))
        self.ICtb.append(str(G))
        self.ICtb.append(" M ".center(80, '-'))
        self.ICtb.append(str(M))
        self.ICtb.append(" I ".center(80, '-'))
        self.ICtb.append(str(I))
        self.ICtb.append(" K ".center(80, '-'))
        self.ICtb.append(str(K))

        return K

    def CA(self, A):
        pass

    def CO(self, B):
        pass

    # ICtextBrowser clear 함수
    def IC_clear_text(self):
        self.ICtb.clear()

    # CAtextBrowser clear 함수
    def CA_clear_text(self):
        self.CAtb.clear()

    # COtextBrowser clear 함수
    def CO_clear_text(self):
        self.COtb.clear()

# FormalConcept Tab
class FCTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        pass

    def extractConcepts(self, formal_context):
        pass

    def powerset(self, array):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FCAwithGUI()
    sys.exit(app.exec_())
