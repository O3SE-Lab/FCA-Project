# FCA with GUI
# 2018210032 김태영

# [현재까지 진행 사항]
# InputContext 부분 GUI 및 구현 완료, CA CO 부분 GUI 완료 but 구현에서 문제가 생겨 CA CO팀 도움 필요, Formal Concept GUI 및 구현 시작 필요
# 이전 버전에서 변경 사항 : GUI 레이아웃을 그리드 레이아웃에서 박스 레이아웃으로 변경, InputContext 와 CA CO 부분을 탭을 이용해 쉽게 볼 수 있도록 배치

# [이번주 진행할 사항]
# FCA 프로그램 제작 완료하기(일부 변수명 의미있게 수정, CA CO 구현 부분 문제 해결 및 구현 완료하기, Context 입력(open csv file) 부분을 탭 밖(탭 윗부분)에 배치하여 Context 입력은 한번만 해도 되도록 배치, Formal Concept GUI & 구현 가능하게)

# 만들 때 참고한 사이트 : https://wikidocs.net/book/2165


import pandas as pd
import sys
from PyQt5.QtWidgets import *

# Widget : 화면에 표시할 수 있는 것을 목적으로 함. ex) 버튼, 사용자 입력 등
# Dialog : MainWindow의 특별한 종류. 대화상자가 항상 별도의 창에 표시되는 최상위 위젯(다른 위젯에 넣을 수 없음)
# MainWindow : 메뉴바, 스테이터스바 등 미리 설정되어있는 최상위 위젯

#-----------------------------------------------
# Main
class FCAwithGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 탭 생성
        tabs = QTabWidget()
        tabs.addTab(ICTab(), 'InputContext')
        tabs.addTab(CACOTab(), 'CACO')
        tabs.addTab(FCTab(), 'FormalConcept')

        # 박스 레이아웃을 이용해 배치
        vbox = QVBoxLayout()
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
#-----------------------------------------------


#-----------------------------------------------
# InputContext Tab
class ICTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # InputContext - 라벨들 생성
        ICtitleL = QLabel('[ Context 입력 ]') # context 입력 타이틀 라벨
        ICfptitleL = QLabel('  선택 파일(*.csv) : ', self)  # 선택 파일 타이틀 라벨
        self.ICfilePathL = QLabel('', self)  # 선택한 파일 경로를 보여줄 라벨

        ICresultTitleL = QLabel('[ Input Context 실행결과 ]', self)  # IC 실행결과 타이틀 라벨

        # InputContext - 실행 결과 출력할 텍스트 브라우저 생성
        self.ICtb = QTextBrowser()

        # InputContext - 파일 오픈 및 실행, CLEAR 버튼 생성
        ICfileOpenB = QPushButton('Context 입력(Open CSV File)', self) # context 입력 버튼
        ICfileOpenB.clicked.connect(self.csv_open) # 버튼 클릭 시 csv_open() 실행

        ICexcuteB = QPushButton('실행', self) # 실행 버튼
        ICexcuteB.clicked.connect(self.IC_clear_text) # 실행버튼 클릭 시 결과 출력되는 텍스트 브라우저 초기화(IC_clear_text())
        ICexcuteB.clicked.connect(lambda: self.ICresult(self.InputContext(self.ICfilePathL.text()))) # 실행버튼 클릭 시 ICresult(InputContext(ICfilePathL.text())) 실행

        clearB = QPushButton('CLEAR', self) # clear 버튼
        clearB.clicked.connect(self.IC_clear_text) # clear 버튼 클릭 시 텍스트 브라우저 초기화(IC_clear_text())

        # 박스레이아웃을 사용한 배치
        # InputContext - 선택 파일 경로 표시
        Lhbox = QHBoxLayout() # 선택 파일 : 파일경로(.csv) 나올 수 있게 수평 박스(hbox)에 배치. 라벨이라 L붙여서 변수명을 Lhbox로 정함
        Lhbox.addWidget(ICfptitleL) # '선택파일' 라벨
        Lhbox.addWidget(self.ICfilePathL) # 파일경로 라벨
        Lhbox.addStretch() # 나머지 빈공간

        # InputContext - Context open 실행 및 Clear 버튼
        Bhbox = QHBoxLayout() # context open 버튼, 실행 버튼, clear 버튼 수평 박스(hbox)에 배치. 버튼이라 B붙여서 변수명을 Bhbox로 정함
        Bhbox.addWidget(ICfileOpenB) # context open 버튼
        Bhbox.addWidget(ICexcuteB) # 실행 버튼
        Bhbox.addWidget(clearB) # clear 버튼

        # 수직 박스(vbox)에 다 넣어줌
        vbox = QVBoxLayout()
        vbox.addWidget(ICtitleL)
        vbox.addLayout(Lhbox)
        vbox.addWidget(ICresultTitleL)
        vbox.addWidget(self.ICtb)
        vbox.addLayout(Bhbox)
        self.setLayout(vbox)

    # Input Context 실행 함수
    def InputContext(self, fPath):

        data = pd.read_csv(fPath) # fPath = 선택한 파일 경로

        # G : 객체들의 집합, M : 속성들의 집합, I : 객체와 속성 사이의 관계 집합 (I ⊆ G × M). 따라서 list가 아닌 set으로.
        G = set(data.index)
        M = set(data.columns)
        I = set()

        # Process : Formal Context를 읽어들여서 "적절한 Data구조 K"에 저장". formal context K:=(G, M, I)
        for g in G:
            for m in M:
                if data[m][g] in ['x', 'X']:
                    I.add((g, m))

        K = [G, M, I]

        return K

    def ICresult(self, K):
        G = K[0]
        M = K[1]
        I = K[2]

        # G 결과 출력
        self.ICtb.append(" G ".center(110, '-'))
        self.ICtb.append(str(G))
        # M 결과 출력
        self.ICtb.append(" M ".center(110, '-'))
        self.ICtb.append(str(M))
        # I 결과 출력
        self.ICtb.append(" I ".center(111, '-'))
        self.ICtb.append(str(I))
        # K 결과 출력
        self.ICtb.append(" K ".center(111, '-'))
        self.ICtb.append(str(K))

    def csv_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './', 'csv(*.csv)') # 세번쨰 매개변수는 기본경로 설정. 안하면  모든파일(*)로 됨
        self.ICfilePathL.setText(fname[0]) # 파일 경로 보여주는 라벨의 text를 파일 경로로 설정
        self.ICtb.clear() # 결과창(텍스트 브라우저) clear

    # ICtextBrowser clear 함수
    def IC_clear_text(self):
        self.ICtb.clear()
#-----------------------------------------------

#-----------------------------------------------
# CA CO Tab
class CACOTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # InputContext - 라벨, 버튼, 텍스트브라우저 생성
        ICtitleL = QLabel('[ Context 입력 ]') # context 입력 타이틀 라벨
        ICfptitleL = QLabel('  선택 파일(*.csv) : ', self)  # 선택 파일 타이틀 라벨
        self.ICfilePathL = QLabel('', self)  # 선택한 파일 경로를 보여줄 라벨

        ICresultTitleL = QLabel('[ Input Context 실행결과 ]', self)  # IC 실행결과 타이틀 라벨
        self.ICtb = QTextBrowser() # IC 실행 결과 출력할 텍스트 브라우저

        ICfileOpenB = QPushButton('Context 입력(Open CSV File)', self) # context 입력 버튼
        ICfileOpenB.clicked.connect(self.csv_open) # 버튼 클릭 시 csv_open() 실행

        ICexcuteB = QPushButton('실행', self) # 실행 버튼
        ICexcuteB.clicked.connect(self.IC_clear_text) # 버튼 클릭 시 결과창 clear 후
        ICexcuteB.clicked.connect(lambda: self.ICresult(self.InputContext(self.ICfilePathL.text()))) # 결과 출력

        clearB = QPushButton('CLEAR', self) # clear 버튼
        clearB.clicked.connect(self.IC_clear_text) # 버튼 클릭 시 ICtb(결과창(텍스트브라우저)) clear

        # 구분 경계선 --- 이런거
        jtextL = QLabel('-' * 118)

        #CA
        jtext2L = QLabel('-' * 118)

        # CACO - 라벨 생성 및 설정
        CAtitleL = QLabel('[CA]', self)  # CA 타이틀 라벨
        CAresultTitleL = QLabel('[CA 실행결과]', self)  # CA 실행결과 타이틀 라벨

        COtitleL = QLabel('[CO]', self)  # CO 타이틀 라벨
        COresultTitleL = QLabel('[CO 실행결과]', self)  # CO 실행결과 타이틀 라벨

        # 텍스트 에디터 생성 및 설정
        self.CAte = QTextEdit() # CA 입력받을 텍스트에디터
        self.CAte.setAcceptRichText(False) # setAcceptRichText를 False로 하면 모두 플레인 텍스트로 인식
        self.COte = QTextEdit() # CO 입력받을 텍스트에디터
        self.COte.setAcceptRichText(False)  # setAcceptRichText를 False로 하면 모두 플레인 텍스트로 인식

        # 버튼 생성 및 설정
        # CA
        CAexcuteB = QPushButton('실행', self)
        CAclearB = QPushButton('CLEAR', self)
        CAexcuteB.clicked.connect(self.CA_clear_text)
        CAexcuteB.clicked.connect(lambda: self.CA(self.CAte.toPlainText()))

        # CO
        COexcuteB = QPushButton('실행', self)
        COclearB = QPushButton('CLEAR', self)
        COexcuteB.clicked.connect(self.CO_clear_text)
        COexcuteB.clicked.connect(lambda: self.CO(self.COte.toPlainText()))

        # InputContext - 실행 결과 출력 화면 생성
        self.CAtb = QTextBrowser()

        # InputContext - 실행 결과 출력 화면 생성
        self.COtb = QTextBrowser()

        # 박스레이아웃을 사용한 배치 (변수명 좀 더 의미있게 수정 필요)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(ICfptitleL)
        hbox1.addWidget(self.ICfilePathL)
        hbox1.addStretch()

        hbox2 = QHBoxLayout()
        hbox2.addWidget(ICfileOpenB)
        hbox2.addWidget(ICexcuteB)
        hbox2.addWidget(clearB)

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
        hbox6.addWidget(self.CAte)
        hbox6.addWidget(self.CAtb)

        hbox7 = QHBoxLayout()
        hbox7.addWidget(COtitleL)
        hbox7.addWidget(COresultTitleL)

        hbox8 = QHBoxLayout()
        hbox8.addWidget(self.COte)
        hbox8.addWidget(self.COtb)

        vbox = QVBoxLayout()
        vbox.addWidget(ICtitleL)
        vbox.addLayout(hbox1)
        vbox.addWidget(ICresultTitleL)
        vbox.addWidget(self.ICtb)
        vbox.addLayout(hbox2)
        vbox.addWidget(jtextL)

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

        return K

    def ICresult(self, K):
        G = K[0]
        M = K[1]
        I = K[2]

        self.ICtb.append(" G ".center(110, '-'))
        self.ICtb.append(str(G))
        self.ICtb.append(" M ".center(110, '-'))
        self.ICtb.append(str(M))
        self.ICtb.append(" I ".center(111, '-'))
        self.ICtb.append(str(I))
        self.ICtb.append(" K ".center(111, '-'))
        self.ICtb.append(str(K))

    # CA 검토 or 수정 필요
    def CA(self, A):
        K = self.InputContext(self.ICfilePathL.text())
        I = K[2]

        M = []
        A_Prime = []

        AL = []
        AL = A.split(',')

        for a in AL:
            # 임시적으로 저장할 리스트
            temp = []

            # I에서 A의 요소들의 속성들을 가져와 M에 저장
            for i in I:
                if i[0] == a:
                    temp.append(i[1])
            M.append(temp)

        if len(M) != 0:  # 공집합일 경우를 제외

            # M에서 비교하여 공통적인 m들을 구함
            for m in M[0]:
                is_in = False  # 모두 포함하는지 확인할 boolean
                for i in range(len(M)):
                    if m in M[i]:
                        if i == (len(M) - 1):  # 마지막까지 포함하면 is_in을 True로 바꿈
                            is_in = True
                        continue

                    # 없는경우 에는 루프를 끊음
                    else:
                        break

                # is_in이 True일경우 A_Prime에 넣음
                if is_in:
                    A_Prime.append(m)

        self.CAtb.append(A_Prime)

        return A_Prime

    # CO 검토 or 수정 필요
    def CO(self, B):
        # g들을 집어넣을 리스트
        G = []

        # B_Prime 리스트
        B_Prime = []

        for b in B:
            # 임시적으로 저장할 리스트
            temp = []

            # I에서 B의 요소들의 속성들을 가져와 G에 저장
            for i in K[2]:
                if i[1] == b:
                    temp.append(i[0])
            G.append(temp)

        # G에서 비교하여 공통적인 g들을 구함
        for g in G[0]:
            is_in = False  # 모두 포함하는지 확인할 boolean
            for i in range(len(G)):
                if g in G[i]:
                    if i == (len(G) - 1):  # 마지막까지 포함하면 is_in을 True로 바꿈
                        is_in = True
                    continue

                # 없는경우 에는 루프를 끊음
                else:
                    break

            # is_in이 True일경우 B_Prime에 넣음
            if is_in:
                B_Prime.append(g)

        return B_Prime


    def csv_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './', 'csv(*.csv)')
        self.ICfilePathL.setText(fname[0])
        self.ICtb.clear()

    # ICtextBrowser clear 함수
    def IC_clear_text(self):
        self.ICtb.clear()

    # CAtextBrowser clear 함수
    def CA_clear_text(self):
        self.CAtb.clear()

    # COtextBrowser clear 함수
    def CO_clear_text(self):
        self.COtb.clear()
#-----------------------------------------------

#-----------------------------------------------
# FormalConcept tab
class FCTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        pass
#-----------------------------------------------

# main 실행
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FCAwithGUI()
    sys.exit(app.exec_())
