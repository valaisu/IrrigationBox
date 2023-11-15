import cv2
import numpy as np
import random
import copy
from matplotlib import pyplot as plt


# TODO: improve the generation of initial points for the regions
# TODO: improve style
# TODO thicken borders!!!


class Region:
    def __init__(self, code, edges):
        self.code = code
        self.edges = edges
        self.center = []
        self.isGreen = False

    def coords(self):
        return self.edges

    def full_region(self):
        return self.edges + self.center

    def update(self, expanded):
        self.center += self.edges
        self.edges = expanded

    def og_pixels(self, og_image):
        return [og_image[c[0]][c[1]] for c in self.full_region()]


# image dimensions
x, y, w, h = 150, 50, 880, 680

# Read the image
img_color = cv2.imread('plant3.jpg')[y:y+h, x:x+w]


image = cv2.imread('plant3.jpg', cv2.IMREAD_GRAYSCALE)
image_cropped = image[y:y+h, x:x+w]
blurred = cv2.GaussianBlur(image_cropped, (5, 5), 0)
image_edges = cv2.Canny(blurred, 50, 150)





regions_map = [[0]*len(image_cropped[0]) for _ in range(len(image_cropped))]
for i in range(len(image_edges)):
    for j in range(len(image_edges[0])):
        if image_edges[i][j] != 0:
            regions_map[i][j] = 255





def generate_centers(image: list[list[int]], tile_size=25):

    w, h = len(image[0]), len(image)
    tile_w = tile_size
    tile_h = tile_size
    # generate the centers of the areas
    x_centers = np.linspace(round(tile_w/2), w-round(tile_w/2), int(round(w/tile_w)))
    y_centers = np.linspace(round(tile_h/2), h-round(tile_h/2), int(round(h/tile_h)))
    region_list = []
    tot_regions = len(x_centers)*len(y_centers)
    random_codes = random.sample(range(1000, 1001+tot_regions*5), tot_regions)
    counter = 0
    for i in range(len(x_centers)):
        for j in range(len(y_centers)):
            region_list.append(
                Region(
                    random_codes[counter],
                    [(int(y_centers[j]), int(x_centers[i]))]
            ))
            counter += 1
    return region_list


def expand_edges(reg_map):
    new_edges = []
    for i in range(len(reg_map)):
        for j in range(len(reg_map[i])):
            coord = reg_map[i][j]
            if coord == 255:
                neigh = [(-1, 0), (0, -1), (0, 1), (1, 0)]
                for n in neigh:
                    try:
                        candidate = (i + n[0], j + n[1])
                        if candidate not in new_edges:
                            if reg_map[candidate[0]][candidate[1]] != 255:
                                new_edges.append(candidate)
                    except IndexError:
                        pass
    for e in new_edges:
        reg_map[e[0]][e[1]] = 255

def update_region(region: Region, reg_map: list[list[int]]):
    # naive way of expanding the regions
    new_region = []
    for coord in region.edges:
        neigh = [(-1, -1),(-1, 0),(-1, 1),(0, -1),(0, 1),(1, -1),(1, 0),(1, 1)]
        #neigh = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        for n in neigh:
            candidate = (coord[0]+n[0], coord[1]+n[1])
            try:
                if candidate not in region.center and candidate not in region.edges:
                    if reg_map[candidate[0]][candidate[1]] == 0:
                        if candidate not in new_region:
                            new_region.append(candidate)
            except IndexError:
                pass
    region.update(new_region)
    for pixel in new_region:
        reg_map[pixel[0]][pixel[1]] = region.code


def visualize(table):
    plt.imshow(np.array(table))
    plt.show()


# generate the regions
region_list = generate_centers(img_color, 15)


visualize(regions_map)
for i in range(1): expand_edges(regions_map)


for i in range(50):
    for r in region_list:
        update_region(r, regions_map)

visualize(regions_map)


def is_green(pixels, tolerance_r: float, tolerance_b: float):
    r_sum, g_sum, b_sum = 0, 0, 0
    for p in pixels:
        r_sum += p[2]
        g_sum += p[1]
        b_sum += p[0]
    r_sum /= len(pixels)
    g_sum /= len(pixels)
    b_sum /= len(pixels)

    if g_sum*tolerance_b >= b_sum and g_sum*tolerance_r >= r_sum:
        return True
    else:
        return False


new_col_im = copy.deepcopy(img_color)
new_list = [[0]*len(image_cropped[0]) for _ in range(len(image_cropped))]

for r in region_list:
    c = 0
    if is_green(r.og_pixels(img_color), 1.15, 0.65):
        c = 1
    for pixel in r.full_region():
        new_list[pixel[0]][pixel[1]] = c
        if c == 1:
            new_col_im[pixel[0]][pixel[1]][1] = 255

visualize(new_list)

cv2.imshow("edges1", new_col_im)
cv2.waitKey(0)
cv2.destroyAllWindows()

visualize(regions_map)

