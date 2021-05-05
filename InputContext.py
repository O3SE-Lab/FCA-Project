"""
pandas 라이브러리 사용
pandas dataframe 활용
"""

import pandas as pd



def InputContext(file):

    #csv read
    df = pd.read_csv(file)

    #Row
    G = list(df['0'].head())

    #column
    M = list(df.columns[1:])

    #G,M들의 set
    I = []

    for i in range(len(G)):
        for j in range(len(M)):
            if df[M[j]][i] == 1:
                I.append((G[i],M[j]))
    K = [G,M,I]

    return K


#---------Main----------------------
data = InputContext("./TestData.csv")
mf_data = data[2:]

print(mf_data)

#data = "./TestData.csv"
#df = pd.read_csv(data)
#print(df)
