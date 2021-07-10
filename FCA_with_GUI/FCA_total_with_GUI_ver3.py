# FCA with GUI
# 2018210032 김태영

# 최근 수정 날짜 : 2021.07.10

# [진행 완료 사항]
# Context 입력(open csv file) 부분을 탭 밖(탭 윗부분)에 배치, 탭 밖(탭 윗부분)에서 받아온 FliePath를 각 클래스가 전달(?)받을 수 있게 완료함, 기능 함수들을 각 클래스로 만들어 상속받게 함
# 이전 버전에서 변경 사항
# : Context 입력(open csv file) 부분을 탭 밖(탭 윗부분)에 배치해 Context 입력은 한번만 해도 되도록 배치,
#   InputContext / CACO / FormalConcept 에서 필요한 기능 함수들을 각 클래스로 만들어 상속받아 사용할 수 있게 하여 기능 구현 함수들을 중복으로 적지 않아도 되도록 함.

# [진행 해야 할 사항]
# - 일부 변수명 의미있게 수정
# - CA CO def 구현 부분 문제 해결
# - Formal Concept def EC() 구현 마무리

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
        # super로 기반 클래스의 __init__ 메서드 호출
        super().__init__()
        #변수 초기화
        self.ICfilePathL = None
        self.icT = None
        self.cacoTab = None
        self.fcTab = None
        # initUI() 실행
        self.initUI()

    def initUI(self):
        # Context 입력 - 라벨 생성
        ICtitleL = QLabel('[ Context 입력 ]')  # context 입력 타이틀 라벨
        ICfptitleL = QLabel('  선택 파일(*.csv) : ', self)  # 선택 파일 타이틀 라벨
        self.ICfilePathL = QLabel('', self)  # 선택한 파일 경로를 보여줄 라벨

        # Context 입력 - 버튼 생성
        ICfileOpenB = QPushButton('Context 입력(Open CSV File)', self)  # context 입력 버튼(csv 파일 open 버튼)
        ICfileOpenB.pressed.connect(self.csv_open)  # 버튼 클릭 시 csv_open()실행

        # 탭 생성
        tabs = QTabWidget()
        self.icT = ICTab() # InputContext Tab
        self.cacoTab = CACOTab() # CACO Tab
        self.fcTab = FCTab() # FormalConcept Tab
        tabs.addTab(self.icT, 'InputContext')
        tabs.addTab(self.cacoTab, 'CACO')
        tabs.addTab(self.fcTab, 'FormalConcept')

        # 박스 레이아웃을 이용해 배치
        hbox1 = QHBoxLayout()
        hbox1.addWidget(ICfptitleL)
        hbox1.addWidget(self.ICfilePathL)
        hbox1.addStretch()

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
        self.icT.setFileName(fname[0])
        self.fcTab.setFileName(fname[0])
        self.cacoTab.setFileName(fname[0])
        self.ICfilePathL.setText(fname[0])
#---------------------------------------------------------

#---------------------------------------------------------
# 기능 구현 클래스들
# InputContext 기능 구현 함수가 있는 클래스
class FcaInputContext:
    def __init__(self):
        self.fileName = None

    # 파일 경로 받아오는 함수
    def setFileName(self, fileName):
        self.fileName = fileName

    # Input Context 실행 함수
    def InputContext(self):
        data = pd.read_csv(self.fileName)

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

# CACO 기능 구현 함수가 있는 클래스 (FcaInputContext 클래스를 상속 받음)
class FcaCACO(FcaInputContext):
    def __init__(self):
        super().__init__()

    def CA(self, A):
        pass

    def CO(self, B):
        pass

# FormalConcept 기능 구현 함수가 있는 클래스 (FcaCACO 클래스를 상속 받음)
class FcaFormalConcept(FcaCACO):
    def __init__(self):
        super().__init__()

    def powerset(self, array):
        set_size = len(array)
        set_pow = []

        for i in range(2 ** set_size):
            flag = bin(i)[2:].zfill(set_size)
            subset = [array[j] for j in range(set_size) if flag[j] == '1']
            set_pow.append(set(subset))
        return set_pow

    def extractConcepts(self):
        pass

#---------------------------------------------------------

#---------------------------------------------------------
# Tab들
# InputContext Tab
class ICTab(QWidget, FcaInputContext):
    def __init__(self):
        super().__init__()
        self.ICexcuteB = None
        self.initUI()

    def initUI(self):
        # InputContext - 라벨 생성
        ICresultTitleL = QLabel('[ Input Context 실행결과 ]', self)  # IC 실행결과 타이틀 라벨

        # InputContext - 실행 결과 출력할 텍스트 브라우저 생성
        self.ICtb = QTextBrowser()

        # InputContext - 파일 오픈 및 실행, CLEAR 버튼 생성
        self.ICexcuteB = QPushButton('실행', self)
        self.ICexcuteB.clicked.connect(self.IC_clear_text)  # 실행버튼 클릭 시 결과 출력되는 텍스트 브라우저 초기화(IC_clear_text())
        self.ICexcuteB.clicked.connect(lambda: self.ICresult())

        clearB = QPushButton('CLEAR', self)
        clearB.clicked.connect(self.IC_clear_text)

        # 박스레이아웃을 사용한 배치
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.ICexcuteB)
        hbox2.addWidget(clearB)

        vbox = QVBoxLayout()
        vbox.addWidget(ICresultTitleL)
        vbox.addWidget(self.ICtb)
        vbox.addLayout(hbox2)
        self.setLayout(vbox)

    # InputContext 결과 출력 함수
    def ICresult(self):
        K = self.InputContext()
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

    # ICtextBrowser clear 함수
    def IC_clear_text(self):
        self.ICtb.clear()


# CA CO Tab
class CACOTab(QWidget, FcaCACO):
    def __init__(self):
        super().__init__()
        self.CAtb = None
        self.COtb = None
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
        self.CAtb = QTextBrowser()
        self.COtb = QTextBrowser()

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
        hbox6.addWidget(self.CAtb)

        hbox7 = QHBoxLayout()
        hbox7.addWidget(COtitleL)
        hbox7.addWidget(COresultTitleL)

        hbox8 = QHBoxLayout()
        hbox8.addWidget(COte)
        hbox8.addWidget(self.COtb)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
        vbox.addLayout(hbox3)
        vbox.addWidget(jtext2L)
        vbox.addLayout(hbox7)
        vbox.addLayout(hbox8)
        vbox.addLayout(hbox4)
        self.setLayout(vbox)

    # CAtextBrowser clear 함수
    def CA_clear_text(self):
        self.CAtb.clear()

    # COtextBrowser clear 함수
    def CO_clear_text(self):
        self.COtb.clear()


# FormalConcept tab
class FCTab(QWidget, FcaFormalConcept):
    def __init__(self):
        super().__init__()
        self.GMselectC = None
        self.PStb = None
        self.ECtb = None
        self.initUI()

    def initUI(self):
        # FormalConcept
        # FormalConcept - 라벨 생성 및 설정
        PSresultTitleL = QLabel('[Powerset 실행결과]', self)  # PS 실행결과 타이틀 라벨
        FCresultTitleL = QLabel('[FormalConcept 실행결과]', self)  # FC 타이틀 라벨

        # Powerset - G, M 선택 콤보 박스
        self.GMselectC = QComboBox()
        self.GMselectC.addItem("G")
        self.GMselectC.addItem("M")

        # PS - 실행 결과 출력 화면 생성
        self.PStb = QTextBrowser()

        # EC - 실행 결과 출력 화면 생성
        self.ECtb = QTextBrowser()

        # 버튼 생성 및 설정
        # PS
        PSexcuteB = QPushButton('실행', self)
        PSclearB = QPushButton('CLEAR', self)
        PSexcuteB.clicked.connect(self.PS_clear_text)
        PSexcuteB.clicked.connect(lambda: self.resultPS(self.InputContext()[0]) \
            if self.GMselectC.currentText() == "G" else self.resultPS(self.InputContext()[1]))
        # EC
        ECexcuteB = QPushButton('실행', self)
        ECclearB = QPushButton('CLEAR', self)
        ECexcuteB.clicked.connect(self.EC_clear_text)
        ECexcuteB.clicked.connect(lambda: self.extractConcepts(self.InputContext()))

        # 구분 경계선 --- 이런거
        jtextL = QLabel('-' * 118)

        # 박스레이아웃을 사용한 배치 (변수명 좀 더 의미있게 수정 필요)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.GMselectC)
        hbox3.addStretch()

        hbox4 = QHBoxLayout()
        hbox4.addWidget(PSexcuteB)
        hbox4.addWidget(PSclearB)

        hbox5 = QHBoxLayout()
        hbox5.addWidget(ECexcuteB)
        hbox5.addWidget(ECclearB)

        vbox = QVBoxLayout()
        vbox.addWidget(PSresultTitleL)
        vbox.addLayout(hbox3)
        vbox.addWidget(self.PStb)
        vbox.addLayout(hbox4)
        vbox.addWidget(FCresultTitleL)
        vbox.addWidget(self.ECtb)
        vbox.addLayout(hbox5)

        self.setLayout(vbox)

    def resultPS(self, SS):
        self.PStb.append(str(self.powerset(list(SS))))

    def PS_clear_text(self):
        self.PStb.clear()

    def EC_clear_text(self):
        self.ECtb.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FCAwithGUI()
    sys.exit(app.exec_())
