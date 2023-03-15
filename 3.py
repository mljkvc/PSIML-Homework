import numpy as np
from math import sqrt, pi, cos, sin
from PIL import Image, ImageFilter, ImageDraw
import PIL.PngImagePlugin as png
import time
from collections import defaultdict

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
    res = []
    while True:
        #za svaku boju kruga zovem fju nadji
        k1 = nadji(krugovi, 'B', 'Y')
        k2 = nadji(krugovi, 'Y', 'B')
        k3 = nadji(krugovi, 'Y', 'K')
        k4 = nadji(krugovi, 'K', 'G')
        k5 = nadji(krugovi, 'G', 'R')

        if k1 == 0 or k2 == 0 or k3 == 0 or k4 == 0 or k5 == 0: 
            break

        krugovi.remove(k1)
        krugovi.remove(k2)
        krugovi.remove(k3)
        krugovi.remove(k4)
        krugovi.remove(k5)
        
        res.append(k1)
        res.append(k2)
        res.append(k3)
        res.append(k4)
        res.append(k5)

        br_validnih += 1
    #----------------------------

    #ispis task2
    print(br_validnih)
    for i in res:
        print(i[0], i[1], i[2])
    #----------------------------

#hough_circles algoritam za trazenje centrova krugova
def hough_circles(img, rmin, rmax, steps, threshold):

    #grayscale, edge detector
    gray = img.convert('L')
    pom = np.where(np.array(gray) > 240, 255, 0)
    gray.putdata(pom.flatten())
    #---------------------------

    #nadji koordinate svih crnih pixela
    pixels = np.asarray(gray)
    koordinate = np.column_stack(np.where(pixels < 10))
    koordinate = koordinate.tolist()
    #---------------------------
    
    #nije mi najjasnije sta se nalazi u points
    points = []
    for r in range(rmin, rmax + 1):
        for t in range(steps):
            points.append((r, int(r * cos(2 * pi * t / steps)), int(r * sin(2 * pi * t / steps))))
    #---------------------------

    #nije mi ni najjasnije sta se ovde radi popunjava se direktorijum? sa 
    acc = defaultdict(int)
    for y, x in koordinate:
        for r, dx, dy in points:
            a = x - dx
            b = y - dy
            acc[(a, b, r)] += 1
    #---------------------------

    #nije mi ni ovo najjasnije, ovde popunjavamo circles sa bojom, koordinatama centrova i poluprecnikom
    circles = []
    for k, v in sorted(acc.items(), key=lambda i: -i[1]):
        x, y, r = k
        if v / steps >= threshold and all((x - xc) ** 2 + (y - yc) ** 2 > rc ** 2 for _, xc, yc, rc in circles):     
            #uzimamo rgb vrednosti iz slike da bi upisali boju
            rgb_im = img.convert('RGB')
            rgb = rgb_im.getpixel((x + r, y))
            if rgb in boje:
                circles.append((boje[rgb], x, y, r))
    #----------------------------

    #pozivam ispis
    ispis(circles)
    

#main

path = input()
img = Image.open(path)
# img = Image.open("/home/covek/Downloads/PSIML/4204/Olympic_rings/public/set/02.png")
task1(img)
hough_circles(img, 50, 89, 17, 0.4)

#------------------------