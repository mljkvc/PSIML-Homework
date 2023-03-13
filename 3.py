import numpy as np
from math import sqrt, pi, cos, sin
from PIL import Image, ImageFilter, ImageDraw
import PIL.PngImagePlugin as png

#task 1 radi super
def task1(img):

    boje = {
        (255, 0, 0): 'red',
        (0, 0, 255): 'blue',
        (0, 255, 0): 'green',
        (255, 255, 0): 'yellow',
        (0, 0, 0): 'black'
    }

    brojac = {
        'red': 0,
        'blue': 0,
        'green': 0,
        'yellow': 0,
        'black': 0
    }

    for pixel in img.getdata():
        if pixel in boje:
            brojac[boje[pixel]] += 1

    for n, m in brojac.items():
        print(m)

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
    grej = np.where(np.asarray(gray) > 240, 255, 0).astype('uint8')
    grej2 = Image.fromarray(grej, mode='L')
    edges = grej2.filter(ImageFilter.FIND_EDGES)
    pom = np.where(np.array(edges) > 15, 255, 0)
    edges.putdata(pom.flatten())
    # edges.show()

    #ide kroz sliku i gleda ako pixel nije crn
    for x in range(width):
        for y in range(height):
            if edges.getpixel((x, y)) != 0: 
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
    


# path = input()
# img = Image.open(path)
img = Image.open("logo.png")
task1(img)
hough(img, 150, 271)



