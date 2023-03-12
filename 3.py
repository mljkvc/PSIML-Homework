import numpy as np
from math import sqrt, pi, cos, sin
from PIL import Image, ImageFilter, ImageDraw


boje = {
    (255, 0, 0): 'red',
    (0, 0, 255): 'blue',
    (0, 255, 0): 'green',
    (255, 255, 0): 'yellow',
    (0, 0, 0): 'black'
}

def task1(img):
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


def hough(image, radius, threshold):
    # Convert the image to grayscale
    gray = image.convert('L')
    # Initialize accumulator
    width, height = gray.size
    accumulator = [[0 for y in range(height)] for x in range(width)]

    # Create a lookup table for sin and cos values
    sin_table = [sin(theta) for theta in range(360)]
    cos_table = [cos(theta) for theta in range(360)]

    #edge detector
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edges1 = np.array(edges)
    edges1 = np.where(edges1 > 20, 255, 0)
    edges.putdata(edges1.flatten())

     # Iterate over the edges and vote for circles
    for x in range(width):
        for y in range(height):
            if edges.getpixel((x, y)):
                for theta in range(360):
                    a = int(x - radius * cos_table[theta])
                    b = int(y - radius * sin_table[theta])
                    if a >= 0 and a < width and b >= 0 and b < height:
                        accumulator[a][b] += 1

    # Find the centers of the circles with enough votes
    centers = []
    for x in range(width):
        for y in range(height):
            if accumulator[x][y] >= threshold:
                centers.append((x, y))

    # Draw the circles on a new image
    output = Image.new('RGB', image.size, (255, 255, 255))
    draw = ImageDraw.Draw(output)
    for center in centers:
        draw.ellipse((center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius), outline=(0, 0, 0))
    output.save("da.png")
    



# path = input()
# img = Image.open(path)
img = Image.open("logo.png")
task1(img)
hough(img, 10, 100)


