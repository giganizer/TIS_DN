import json
from collections import Counter
from math import log2
#tega sicer ni treba (je ze v testu)
with open("primeri/1.json","r") as f: #default je "r"
    data = json.load(f)
print(data)

A = data["podatki"]["znacilnice"]
R = list(data["podatki"]["razredi"].values())[0] #iz slovarja vrednosti in v seznam

#to pa je treba

#stevilo zapisov
M = len(R)
assert M == len(A["Nebo"]), "Nekaj je narobe z dolžinami" #preverimo

Az = A["Nebo"]
#unikatni elementi seznama
nodes = set(Az)


#zdruzimo skupaj atribut in razred
AzR = list(zip(Az, R)) #skupaj kot zadrga
print(AzR)

#kateri zapisi so zdaj skupaj v vozliscu
#list comprehension
'''
o = []
for x in AzR:
    if x[0] == "j":
        o.append(x)
'''
leaf_j = [x for x in AzR if x[0]=="j"] #isto kot tiste 4 vrstice, to je list comprehension
leaf_j_class = [x[1] for x in leaf_j]

#koliko jih je v posameznem razredu?
f_j = Counter(leaf_j_class) #razred Counter - to je v resnici histogram


leaf_o = [x for x in AzR if x[0]=="o"] 
leaf_o_class = [x[1] for x in leaf_o]
f_o = Counter(leaf_o_class)

#koliko je zapisov v posameznem listu
n_j = len(leaf_j)
n_o = len(leaf_o)

#nedolocenost
H_j = sum(-(f/n_j)*log2(f/n_j) for f in f_j.values())
H_o = sum(-(f/n_o)*log2(f/n_o) for f in f_o.values())

H = n_j/M * H_j + n_o/M * H_o

#tocnost
majority_j = f_j.most_common(1)
majority_o = f_o.most_common(1)

tocnost = ((majority_j[0][1] + majority_o[0][1])/M)