# FCA 프로그램 제작 프로젝트 
# InputContext_without_Pandas : Formal Context를 입력처리하는 함수(또는 모듈)
# 2018210032 김태영
# 2021.05.08.
import csv

def InputContext(fileName):
    """
    Input : MS Excel파일(csv형식. K := (G,M,I)내용)
    Output : N/A
    """
    f = open(fileName,'r', encoding='utf-8')
    data = list(csv.reader(f))
    
    G = [i[0] for i in data[1:]]
    M = data[0]
    GXM = [i[1:] for i in data[1:]]
    I = []
    
    # Process : Formal Context를 읽어들여서 "적절한 Data구조 K"에 저장"
    # G : 객체들의 집합, M : 속성들의 집합, I : 객체와 속성 사이의 관계 집합 (I ⊆ G × M), formal context K:=(G, M, I)
    for g in range(len(GXM)):
        for m in range(len(GXM[g])):
            if GXM[g][m] in ['x', 'X']:
                I.append((G[g], M[m]))
    
    K = [set(G),set(M),set(I)]
    return(K)
    f.close()
    

# example
csv_FileName = "./TestData.csv"
result = InputContext(csv_FileName)
print(result) 
