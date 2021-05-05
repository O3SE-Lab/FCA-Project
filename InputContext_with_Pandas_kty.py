# FCA 프로그램 제작 프로젝트 
# InputContext_with_Pandas : Formal Context를 입력처리하는 함수(또는 모듈)
# 2018210032 김태영
# 2021.05.05.

import pandas as pd

def InputContext(fileName):
    """
    Input : MS Excel파일(csv형식. K := (G,M,I)내용)
    Output : N/A
    """
    data = pd.read_csv(fileName)
    G = list(data['0'])
    M = list(data.columns[1:])
    I = []

    # Process : Formal Context를 읽어들여서 "적절한 Data구조 K"에 저장"
    for i in range(len(G)):
        for j in M:
            if data[j][i] == 1:
                I.append((G[i],j))
    K = (G,M,I)
    return K


# example
csv_FileName = "./TestData.csv"
result = InputContext(csv_FileName)
print(result)

#----------------------------------------------
# 번외) 딕셔너리 이용
# G 기준
def g_dict_InputContext(fileName):
    data = pd.read_csv(fileName)
    G = list(data['0'])
    M = list(data.columns[1:])
    G_dict = dict()
    for i in range(len(G)):
        answer = []
        for j in M:
            if data[j][i] == 1:
                answer.append(j)
        G_dict[G[i]] = answer
    return G_dict

# M 기준
def m_dict_InputContext(fileName):
    data = pd.read_csv(fileName)
    G = list(data['0'])
    M = list(data.columns[1:])
    M_dict = dict()
    for i in M:
        answer = []
        for j in range(len(G)):
            if data[i][j] == 1:
                answer.append(G[j])
        M_dict[i] = answer
    return M_dict
#----------------------------------------------

