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

    A_Prime = []
    for a in A:
        temp = []
        for i in range(index_A[a][0], index_A[a][1]):
            temp.append(I[i][1])
        M.append(temp)

    if len(M) != 0:  # 공집합일 경우를 제외

        # M에서 비교하여 공통적인 m들을 구함
        for m in M[0]:
            is_in = True

            for i in range(len(M)):
                if m not in M[i]:
                    is_in = False
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
        temp = []
        for i in range(index_B[b][0], index_B[b][1]):
            temp.append(reverse_i[i][1])
        G.append(temp)

    if len(G) != 0:  # 공집합일 경우를 제외

        # G에서 비교하여 공통적인 g들을 구함
        for g in G[0]:
            is_in = True

            for i in range(len(G)):
                if g not in G[i]:
                    is_in = False
                    break

            # is_in이 True일경우 B_Prime에 넣음
            if is_in:
                B_Prime.append(g)
    return B_Prime


def powerset(array):
    set_size = len(array)
    set_pow = []

    for i in range(2 ** set_size):
        flag = bin(i)[2:].zfill(set_size)
        subset = [array[j] for j in range(set_size) if flag[j] == '1']
        set_pow.append(subset)
    # 실행 코드

    return set_pow


def extractConcepts(formal_context):
    FC_set = []  # FC들을 저장할 함수

    A = list(powerset(formal_context[0]))  # 객채들의 부분집합
    B = list(powerset(formal_context[1]))  # 속성들의 부분집합

    for a in A:  # A안의 a와 B안의 b를 서로 비교하여 조건이 맞다면 FC_set에 집어넣음
        for b in B:
            if CA(a) == b:
                if CO(b) == a:
                    FC_set.append([a, b])
                    break  # 넣은 뒤 루프를 끊고 다음루프로 넘어감

    return FC_set

csv_FileName = "./TestData.csv"

K = InputContext(csv_FileName)

index_A = {}
cnt = 0
for i in range(0, len(K[2])-1):
    if(K[2][i][0] != K[2][i+1][0]):
        index_A[K[2][i][0]] = cnt, i
        cnt = i+1
index_A[K[2][i][0]] = cnt, i

index_B = {}

reverse_i = []
for i in K[2]:
    reverse_i.append([i[1],i[0]])
reverse_i = sorted(reverse_i)

cnt = 0
for i in range(0, len(reverse_i)-1):
    if(reverse_i[i][0] != reverse_i[i+1][0]):
        index_B[reverse_i[i][0]] = cnt, i
        cnt = i+1

index_B[reverse_i[i][0]] = cnt, i

print(extractConcepts(K))
