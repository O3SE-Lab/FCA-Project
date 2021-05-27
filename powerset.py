import itertools

def powerset(y):
    S = list(y)
    L = set()
    
    for i in range (0,len(S)+1):
        temp = set(map(tuple, itertools.combinations(S, i)))
        L.update(temp)
    return L

G = {'a1','a2','a3'}
M = {'b1', 'b2', 'b3', 'b4'}
print("powerset(G) = {}".format(powerset(G)))
print("[증명]") # 원소의 개수가 n개인 집합의 부분집합의 개수 : 2**n개 -> 멱집합의 원소의 개수 또한 2**n개
print("len(powerset(G)) = {}".format(len(powerset(G))))
print("2**len(G) = {}".format(2**len(G)))
print("-------------------")
print("powerset(M) = {}".format(powerset(M)))
print("[증명]")
print("len(powerset(M)) = {}".format(len(powerset(M))))
print("2**len(M) = {}".format(2**len(M)))