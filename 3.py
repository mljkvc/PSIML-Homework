import numpy as np
from math import sqrt, pi, cos, sin
from PIL import Image, ImageFilter, ImageDraw
import PIL.PngImagePlugin as png

#task 1 radi super
def task1(img):

    boje = {
        (255, 255, 0): 'Y',
        (0, 0, 255): 'B',
        (0, 0, 0): 'K',
        (0, 255, 0): 'G',
        (255, 0, 0): 'R'
    }

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

#task2 ne radi bas sjajno
def hough(image: png.PngImageFile, radius, threshold):
    #u grayscale
    gray = image.convert('L')
    
    # pravim akumulator
    width, height = gray.size
    accumulator = [[0 for y in range(height)] for x in range(width)]
    # Create a lookup table for sin and cos values?
    sin_table = [sin(teta) for teta in range(360)]
    cos_table = [cos(teta) for teta in range(360)]
    
    #edge detector
    pom = np.where(np.array(gray) > 240, 255, 0)
    gray.putdata(pom.flatten())
    # gray.show()

    #ide kroz sliku i gleda ako pixel nije crn
    for x in range(width):
        for y in range(height):
            if gray.getpixel((x, y)) == 0: 
                for teta in range(360):
                    a = int(x - cos_table[teta])
                    b = int(y - sin_table[teta])
                    if a >= 0 and a < width and b >= 0 and b < height:
                        accumulator[a][b] += 1

    # najgusci presek novonastalih krugova je centar?
    centers = []
    for x in range(width):
        for y in range(height):
            if accumulator[x][y] >= threshold:
                centers.append((x, y))

    #output slika
    output = Image.new('RGB', image.size, (255, 255, 255))
    draw = ImageDraw.Draw(output)
    for center in centers:
        draw.ellipse((center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius), outline=(0, 0, 0))
    output.save("da.png")
    


path = input()
img = Image.open(path)
# img = Image.open("/home/covek/Downloads/PSIML/4204/Olympic_rings/public/set/02.png")
task1(img)
hough(img, 70, 184)



