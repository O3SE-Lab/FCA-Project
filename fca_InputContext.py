#2017210040 조완기

import pandas as pd

def Inputcontext(file):
    data = pd.read_csv(file)

    #Row값을 G집합에 넣는다
    G = list(data['0'])

    #column들을 M집합에 넣는다
    M = list(data.columns[1:])

    I = []

    for i in range(len(G)):
        for j in range(len(M)):
            if data[M[j]][i] == 1:
                #I집합
                I.append((G[i],M[j]))

    K = [G,M,I]