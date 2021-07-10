import pandas as pd
import numpy as np
import time

def InputContext(fileName):
    data = pd.read_csv(fileName)

    G = list(data.index)
    M = list(data.columns)
    I = []

    for i in G:
        for j in M:
            if data[j][i] == "X":
                I.append((i, j))
    K = [G, M, I]
    return K


def CA(A):
    # m들을 집어넣을 리스트
    M = []

    # 전역변수 K에서 I를 가져옴
    I = K[2]

    # A_Prime 리스트
    A_Prime = []
    for a in A:
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
    return A_Prime


def CO(B):
    # g들을 집어넣을 리스트
    G = []

    # 전역변수 K에서 I를 가져옴
    I = K[2]

    # B_Prime 리스트
    B_Prime = []

    for b in B:
        # 임시적으로 저장할 리스트
        temp = []

        # I에서 B의 요소들의 속성들을 가져와 G에 저장
        for i in I:
            if i[1] == b:
                temp.append(i[0])
        G.append(temp)

    if len(G) != 0:  # 공집합일 경우를 제외

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


def powerset(array):
    startTime = time.time()
    set_size = len(array)
    set_pow = []

    for i in range(2 ** set_size):
        flag = bin(i)[2:].zfill(set_size)
        subset = [array[j] for j in range(set_size) if flag[j] == '1']
        set_pow.append(subset)
    # 실행 코드

    endTime = time.time() - startTime
    print("powerset:", endTime)
    return set_pow


def extractConcepts(formal_context):
    startTime = time.time()

    FC_set = []  # FC들을 저장할 함수

    A = list(powerset(formal_context[0]))  # 객채들의 부분집합
    B = list(powerset(formal_context[1]))  # 속성들의 부분집합

    for a in A:  # A안의 a와 B안의 b를 서로 비교하여 조건이 맞다면 FC_set에 집어넣음
        for b in B:
            if CA(a) == b:
                if CO(b) == a:
                    FC_set.append([a, b])
                    break  # 넣은 뒤 루프를 끊고 다음루프로 넘어감


    endTime = time.time() - startTime
    print("FC: ",endTime)
    return FC_set

csv_FileName = "./TestData.csv"

K = InputContext(csv_FileName)
print(extractConcepts(K))
