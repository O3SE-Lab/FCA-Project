# FCA 프로그램 제작 프로젝트 
# InputContext_with_Pandas : Formal Context를 입력처리하는 함수(또는 모듈)
# 2018210032 김태영
# 2021.05.08.

import pandas as pd

def InputContext(fileName):
    """
    Input : MS Excel파일(csv형식. K := (G,M,I)내용)
    Output : N/A
    """
    data = pd.read_csv(fileName)
    
    # G : 객체들의 집합, M : 속성들의 집합, I : 객체와 속성 사이의 관계 집합 (I ⊆ G × M)
    G = set(data.index)
    M = set(data.columns)
    I = set()

    # Process : Formal Context를 읽어들여서 "적절한 Data구조 K"에 저장"
    # formal context K:=(G, M, I)
    for g in G:
        for m in M:
            if data[m][g] in ['x', 'X']:
                I.add((g,m))
    
    K = [G,M,I]
    return K

# example
csv_FileName = "./TestData.csv"
result = InputContext(csv_FileName)
print(result)

#---------------------------------------------------------------
# 번외) 딕셔너리 이용
# G 기준
def g_dict_InputContext(fileName):
    
    data = pd.read_csv(fileName)
    
    # G : 객체들의 집합, M : 속성들의 집합, G_dict : G 기준 딕셔너리
    G = set(data.index)
    M = set(data.columns)
    G_dict = dict()
    
    # Process : Formal Context를 읽어들여서 "적절한 Data구조 G_dict"에 저장"
    for g in G:
        answer = set()
        for m in M:
            if data[m][g] in ['x', 'X']:
                answer.add(m)
        G_dict[g] = answer
    return G_dict

# M 기준
def m_dict_InputContext(fileName):
    
    data = pd.read_csv(fileName)
    
    # G : 객체들의 집합, M : 속성들의 집합, G_dict : G 기준 딕셔너리
    G = set(data.index)
    M = set(data.columns)
    M_dict = dict()
    
    # Process : Formal Context를 읽어들여서 "적절한 Data구조 M_dict"에 저장"
    for m in M:
        answer = set()
        for g in G:
            if data[m][g] in ['x', 'X']:
                answer.add(g)
        M_dict[m] = answer
    return M_dict

# example (print문(line 80-83)은 주석처리 해놓음)
csv_FileName = "./TestData.csv"
g_dict_result = g_dict_InputContext(csv_FileName)
m_dict_result = m_dict_InputContext(csv_FileName)

# print("----------------------------------------------------------------------")
# print("G_dict : ", g_dict_result)
# print("----------------------------------------------------------------------")
# print("M_dict : ", m_dict_result)
#----------------------------------------------
