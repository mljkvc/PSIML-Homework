import sys
import numpy as np
from math import pi


#task1 radi
def task1(brojevi):
    povrs = 6 * len(brojevi)

    for i in range(len(brojevi)):
        for j in range(i+1, len(brojevi)):
            if brojevi[i][0] == brojevi[j][0] and brojevi[i][1] == brojevi[j][1]:
                if abs(brojevi[i][2] - brojevi[j][2]) == 1:
                    povrs -= 2
            if brojevi[i][0] == brojevi[j][0] and brojevi[i][2] == brojevi[j][2]:
                if abs(brojevi[i][1] - brojevi[j][1]) == 1:
                    povrs -= 2
            if brojevi[i][1] == brojevi[j][1] and brojevi[i][2] == brojevi[j][2]:
                if abs(brojevi[i][0] - brojevi[j][0]) == 1:
                    povrs -= 2

    return povrs
#----------------------------

#task2 radi, fali mi edge case za kad nisu povezane celine
def task2(brojevi):

    br_x = {}
    br_y = {}
    br_z = {}
    for i in range(len(brojevi)):
        if brojevi[i][0] not in br_x:
            br_x[brojevi[i][0]] = 1
        else:
            br_x[brojevi[i][0]] += 1
        if brojevi[i][1] not in br_y:
            br_y[brojevi[i][1]] = 1
        else:
            br_y[brojevi[i][1]] += 1
        if brojevi[i][2] not in br_z:
            br_z[brojevi[i][2]] = 1
        else:
            br_z[brojevi[i][2]] += 1

    x = max(br_x.values())
    y = max(br_y.values())
    z = max(br_z.values())
    
    return max(x, y, z)
#----------------------------


#task3
def maxKocka(kocka):
    duz_kocke = len(kocka)
    duz_pr = len(kocka[0])
    lista = []
    for i in range(duz_kocke):
        pom = []
        for j in range(duz_pr):
            if i == 0 or j == 0:
                pom.append(kocka[i][j])
            else:
                pom.append(0)
        lista.append(pom)

    for i in range(1, duz_kocke):
        for j in range(1, duz_pr):
            if kocka[i][j] == 1:
                lista[i][j] = min(lista[i][j - 1], lista[i - 1][j], lista[i - 1][j - 1]) + 1
            else:
                lista[i][j] = 0

    max_value = 0
    for row in lista:
        max_value = max(max_value, max(row))
    return max_value

def task3(brojevi):

    max_x = 0
    max_y = 0
    max_z = 0
    for i in range(len(brojevi)):
        if brojevi[i][0] > max_x:
            max_x = brojevi[i][0]
        if brojevi[i][1] > max_y:
            max_y = brojevi[i][1]
        if brojevi[i][2] > max_z:
            max_z = brojevi[i][2]

    x = []
    y = []
    z = []
    for i in range(max_x + 1):
        pom_y = []
        for j in range(max_y + 1):
            pom_z = []
            for k in range(max_z + 1):
                pom_z.append(0)
            pom_y.append(pom_z)
        x.append(pom_y) 
    for i in range(max_y + 1):
        pom_x = []
        for j in range(max_x + 1):
            pom_z = []
            for k in range(max_z + 1):
                pom_z.append(0)
            pom_x.append(pom_z)
        y.append(pom_x)
    for i in range(max_z + 1):
        pom_x = []
        for j in range(max_x + 1):
            pom_y = []
            for k in range(max_y + 1):
                pom_y.append(0)
            pom_x.append(pom_y)
        z.append(pom_x)
        
    for br in brojevi:
        x[br[0]][br[1]][br[2]] = 1
        y[br[1]][br[0]][br[2]] = 1
        z[br[2]][br[0]][br[1]] = 1

    max_precnik = 1
    for i in range(max_x + 1):
        max_precnik = max(max_precnik, maxKocka(x[i]))
    for i in range(max_y + 1):
        max_precnik = max(max_precnik, maxKocka(y[i]))
    for i in range(max_z + 1):
        max_precnik = max(max_precnik, maxKocka(z[i]))

    povrs = (max_precnik / 2) ** 2 * pi    
    return povrs

#-------------------------------------


#main
brojevi = []
for line in sys.stdin:
    br = [int(x) for x in line.strip().strip('()').split(',')]
    brojevi.append(br)
brojevi = sorted(brojevi)


# print()
# for da in brojevi:
#     print(da)

print(task1(brojevi), task2(brojevi), task3(brojevi))

