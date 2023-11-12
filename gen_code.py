import json
import png
import sys
import math

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

DELTA = 32

def main(desc_json, gradient_png):
    with open(desc_json, 'rt') as f:
        data = json.load(f)

    size = data['size']
    width = size * DELTA * 3
    height = size * DELTA
    particles = data['particles']
    minV = data['min']
    maxV = data['max']

    delta = [1, 1, 1]
    for k in range(3):
        delta[k] = abs(maxV[k] - minV[k])

    data = np.empty([height, width], dtype = int)
    
    for i, p in enumerate(particles):
        c = [255, 0, 0]
        c[2] = int(255 * (abs(p[0] - minV[0]) / delta[0]))
        c[0] = int(255 * (abs(p[1] - minV[1]) / delta[1]))
        c[1] = int(255 * (abs(p[2] - minV[2]) / delta[2]))

        x = (i % size) * DELTA
        y = (i // size) * DELTA 

        for w in range(DELTA):
            x0 = (x + w) * 3
            for h in range(DELTA):
                data[y + h][x0 : x0 + 3] = c

    img = []
    for col in data[:]:
        img.append(col.tolist())
    # for h in range(height):
    #     row = []
    #     for w in range(width):
    #         for k in range(3):
    #             row.appenddata[w][h][k])
            
    #     img.append(row)

    # fig, ax = plt.subplots()
    # x = []
    # y = []
    # for i, p in enumerate(particles):
    #     x.append(p[1])
    #     y.append(p[2])
        
    # #scale = 200.0 * np.random.rand(n)
    # ax.scatter(x, y, c='tab:blue', s=1, label='color',
    #                alpha=0.3, edgecolors='none')

    # ax.legend()
    # ax.grid(True)
    # #plt.show()

    with open(gradient_png, 'wb') as f:
        w = png.Writer(width // 3, height, greyscale=False)
        w.write(f, img)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_json> <output_png>")
    main(*sys.argv[1:])