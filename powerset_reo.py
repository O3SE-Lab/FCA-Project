G = ['x', 'y', 'z']
M = ['b1', 'b2', 'b3', 'b4']

def powerset(array):
    set_size = len(array)
    set_pow = []

    for i in range(2**set_size):
        flag = bin(i)[2:].zfill(set_size)
        subset = [array[j] for j in range(set_size) if flag[j] == '1']
        set_pow.append(subset)
    
    return set_pow
        

print(powerset(G))
print(powerset(M))
