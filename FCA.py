import pandas as pd

def InputContext(fileName):

    data = pd.read_csv(fileName)
    
    G = list(data.index)
    M = list(data.columns)
    I = []
    
    for i in G:
        for j in M:
            if data[j][i] == "X":
                I.append((i,j))
    
    K = [G,M,I]
    array = data.values
    return K

data = InputContext("./TestData.csv")

def CA(A):
      #m들을 집어넣을 리스트
      M = [] 

      #A_Prime 리스트
      A_Prime = []


      for a in A:
        #임시적으로 저장할 리스트
        temp = []

        #I에서 A의 요소들의 속성들을 가져와 M에 저장
        for i in K[2]:
          if i[0] == a:
            temp.append(i[1])
        M.append(temp)

      #M에서 비교하여 공통적인 m들을 구함
      for m in M[0]:
        is_in = False  #모두 포함하는지 확인할 boolean
        for i in range(len(M)):
          if m in M[i]:
            if i == (len(M)-1):  #마지막까지 포함하면 is_in을 True로 바꿈
              is_in = True
            continue

          #없는경우 에는 루프를 끊음
          else:
            break

        #is_in이 True일경우 A_Prime에 넣음
        if is_in:
          A_Prime.append(m)

      return A_Prime

def CO(B):
      #g들을 집어넣을 리스트
      G = []

      #B_Prime 리스트
      B_Prime = []

      for b in B:
        #임시적으로 저장할 리스트
        temp = []

        #I에서 B의 요소들의 속성들을 가져와 G에 저장
        for i in K[2]:
          if i[1] == b:
            temp.append(i[0])
        G.append(temp)

      #G에서 비교하여 공통적인 g들을 구함
      for g in G[0]:
        is_in = False  #모두 포함하는지 확인할 boolean
        for i in range(len(G)):
          if g in G[i]:
            if i == (len(G)-1):  #마지막까지 포함하면 is_in을 True로 바꿈
              is_in = True
            continue

          #없는경우 에는 루프를 끊음
          else:
            break

        #is_in이 True일경우 B_Prime에 넣음 
        if is_in:
          B_Prime.append(g)

      return B_Prime

#PPT의 예제를 사용한 코드

csv_FileName = "./TestData.csv"
K = InputContext(csv_FileName)
A = ["Air Canada", "Air New Zealand", "Scandinavian Airlines"]
B = ["Latin America", "Europe", "United States"]

A_Prime = CA(A)
B_Prime = CO(B)

print(A_Prime)
print(B_Prime)
