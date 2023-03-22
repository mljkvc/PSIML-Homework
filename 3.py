import numpy as np
from math import sqrt, pi, cos, sin
from PIL import Image, ImageFilter, ImageDraw
import PIL.PngImagePlugin as png
import time
from collections import defaultdict
import tracemalloc as t


# t.start()

boje = {
    (255, 255, 0): 'Y',
    (0, 0, 255): 'B',
    (0, 0, 0): 'K',
    (0, 255, 0): 'G',
    (255, 0, 0): 'R'
}

#task 1 radi
def task1(img):

    brojac = {
        'Y': 0,
        'B': 0,
        'K': 0,
        'G': 0,
        'R': 0
    }

    for pixel in img.getdata():
        if pixel[:3] in boje:
            brojac[boje[pixel[:3]]] += 1

    for n, m in brojac.items():
        print(n, m)
#---------------------------

#task2 -----------------------------------------------

#vraca najblizi krug
def nadji(krugovi, boja1, boja2):
        
    min_rast = 800
    min_krug = 0
    for krug1 in krugovi:
        for krug2 in krugovi:
            if krug1[0] == boja1 and krug2[0] == boja2:
                rast = sqrt((krug1[1]-krug2[1])**2+(krug1[2]-krug2[2])**2)
                if rast < min_rast:
                    min_rast = rast
                    min_krug = krug2
    return min_krug
#--------------------------

#ispis za task2
def ispis(krugovi):
    
    #uklanjam poluprecnik iz krugovi
    for i in range(len(krugovi)):
        krugovi[i] = krugovi[i][:3]
    #----------------------------

    #nalazim broj validnih logoa, pronalazim redom za boje i uklanjam ih iz circles i povecavam br
    br_validnih = 0
    pom = []
    while True:
        #za svaku boju kruga zovem fju nadji
        k1 = nadji(krugovi, 'B', 'Y')
        k2 = nadji(krugovi, 'Y', 'B')
        k3 = nadji(krugovi, 'Y', 'K')
        k4 = nadji(krugovi, 'K', 'G')
        k5 = nadji(krugovi, 'G', 'R')

        if k1 == 0 or k2 == 0 or k3 == 0 or k4 == 0 or k5 == 0: 
            break
        
        #ako sam nasao ceo validan logo izbacujem te krugove iz krugovi
        krugovi.remove(k1)
        krugovi.remove(k2)
        krugovi.remove(k3)
        krugovi.remove(k4)
        krugovi.remove(k5)
        
        #pravim pom listu jer moram da ispisem br_validnih pre koordinata
        pom.append(k1)
        pom.append(k2)
        pom.append(k3)
        pom.append(k4)
        pom.append(k5)

        br_validnih += 1
    #----------------------------

    #ispis task2
    print(br_validnih)
    for i in pom:
        print(i[0], i[1], i[2])
    #----------------------------

#hough_circles algoritam za trazenje centrova krugova
def hough_circles(img, r_min, r_max, steps, threshold):

    #uzimam koordinate 
    rgb_im = img.convert('RGB')
    #grayscale, edge detector
    img = img.convert('L')
    img.putdata(np.where(np.array(img) > 240, 255, 0).flatten())
    #---------------------------

    #nadji koordinate svih crnih pixela
    pixels = np.asarray(img)
    koordinate = np.column_stack(np.where(pixels < 10))
    koordinate = koordinate.tolist()
    #---------------------------
    
    #pravimo listu tuplova, uz svaki poluprecnik dodajem x, y koordinatu 
    points = []
    for r in range(r_min, r_max + 1):
        for t in range(steps):
            points.append((r, int(r * cos(2 * pi * t / steps)), int(r * sin(2 * pi * t / steps))))
    #---------------------------

    #popunjavamo accumulator, pravimo krug za svaki pixel na krugu, najveci presek krugova je centar
    accumulator = defaultdict(int)
    for y, x in koordinate:
        for r, dx, dy in points:
            a = x - dx
            b = y - dy
            accumulator[(a, b, r)] += 1
    #---------------------------

    #pronalazimo iz accumulatora poziciju centra kruga i ubacujemo u circles boju centar i poluprecnik
    circles = []
    for k, v in sorted(accumulator.items(), key = lambda i: -i[1]):
        x, y, r = k
        if v / steps >= threshold and all((x - xc) ** 2 + (y - yc) ** 2 > rc ** 2 for _, xc, yc, rc in circles):     
            #uzimamo rgb vrednosti iz slike da bi upisali boju, dodajemo boju u circles
            rgb = rgb_im.getpixel((x + r, y))
            if rgb in boje:
                circles.append((boje[rgb], x, y, r))
    #----------------------------

    #pozivam ispis
    ispis(circles)


#main

path = input()
img = Image.open(path)
task1(img)

#vece vrednosti za r_min r_max i steps ce znatno usporiti program

hough_circles(img, 45, 95, 17, 0.6)




# print(t.get_traced_memory())
# t.clear_traces()
# 500MB  mi zauzima...
#------------------------