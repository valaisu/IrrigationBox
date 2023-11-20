import cv2
import numpy as np
import random
import copy
from matplotlib import pyplot as plt


class Region:
    def __init__(self, code, edges):
        self.code = code
        self.edges = edges
        self.center = []
        self.isGreen = False

    def coordinates(self):
        return self.edges

    def full_region(self):
        return self.edges + self.center

    def update(self, expanded):
        self.center += self.edges
        self.edges = expanded

    def og_pixels(self, og_image):
        return [og_image[c[0]][c[1]] for c in self.full_region()]


def generate_centers(image: list[list[int]], tile_size: int = 25):
    """
    Generates a grid of regions of one pixel. The distance between the regions
    is the tile size.
    :param image: list[list[int]]
    :param tile_size: int
    :return: list[list[int]]
    """
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
    for i in x_centers:
        for j in y_centers:
            region_list.append(
                Region(
                    random_codes[counter],
                    [(int(j), int(i))]
            ))
            counter += 1
    return region_list


def expand_edges(reg_map: list[list[int]]):
    """
    For each pixel in region map, if the pixel is an edge, tries to add
    the four adjacent pixels to edges
    :param reg_map: list[list[int]]
    :return: None
    """
    new_edges = []
    for i, row in enumerate(reg_map):
        for j, elem in enumerate(row):
            coord = elem
            if coord != 255:
                continue
            neigh = [(-1, 0), (0, -1), (0, 1), (1, 0)]
            for n in neigh:
                try:
                    candidate = (i + n[0], j + n[1])
                    if candidate in new_edges:
                        continue
                    if reg_map[candidate[0]][candidate[1]] == 255:
                        continue
                    new_edges.append(candidate)
                except IndexError:
                    pass
    for e in new_edges:
        reg_map[e[0]][e[1]] = 255


def update_region(region: Region, reg_map: list[list[int]]):
    """
    region by region adds all unclaimed neighboring tiles to the region
    quite naive way of expanding the regions
    :param region: Region
    :param reg_map: list[list[int]]
    :return: None
    """
    new_region = []
    for coord in region.edges:
        neigh = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        #neigh = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        for n in neigh:
            candidate = (coord[0]+n[0], coord[1]+n[1])
            try:
                if candidate in region.center or candidate in region.edges:
                    continue
                if reg_map[candidate[0]][candidate[1]] != 0:
                    continue
                if candidate in new_region:
                    continue #break here kinda yields better results
                new_region.append(candidate)
            except IndexError:
                pass
    region.update(new_region)
    for pixel in new_region:
        reg_map[pixel[0]][pixel[1]] = region.code


def visualize(img: list[list[int]], title: str):
    plt.imshow(np.array(img))
    plt.title(title)
    plt.show()


def is_green(pixels: list[list[(int, int, int)]], tolerance_r: float, tolerance_b: float):
    """
    Calculates the average R, G, B values for a region, returns True if
    G*tolerance_b > B and G*tolerance_r > R
    :param pixels: list[list[(int, int, int)]]
    :param tolerance_r: float
    :param tolerance_b: float
    :return: Bool
    """
    r_sum, g_sum, b_sum = 0, 0, 0
    for p in pixels:
        # so apparently the colors are BRG not RGB
        r_sum += p[2]
        g_sum += p[1]
        b_sum += p[0]
    r_sum /= len(pixels)
    g_sum /= len(pixels)
    b_sum /= len(pixels)

    if g_sum*tolerance_b > b_sum and g_sum*tolerance_r > r_sum:
        return True
    else:
        return False


def main():

    # Crop the image
    x, y, w, h = 150, 50, 880, 680

    # Read the image for color detection
    img_color = cv2.imread('plant3.jpg')[y:y+h, x:x+w]

    # Read the image for edge detection
    image = cv2.imread('plant3.jpg', cv2.IMREAD_GRAYSCALE)
    image_cropped = image[y:y+h, x:x+w]
    blurred = cv2.GaussianBlur(image_cropped, (5, 5), 0)
    image_edges = cv2.Canny(blurred, 50, 150)

    # Create the region map, tells us which pixels belong to which region
    regions_map = [[0] * len(image_cropped[0]) for _ in range(len(image_cropped))]
    for i, row in enumerate(image_edges):
        for j, elem in enumerate(row):
            if image_edges[i][j] != 0:
                regions_map[i][j] = 255

    # generate the regions
    region_list = generate_centers(img_color, 15)

    # Make the edges thicker
    for _ in range(1):
        expand_edges(regions_map)

    # Expand the regions
    for _ in range(80):
        for r in region_list:
            update_region(r, regions_map)

    # Show different regions
    visualize(regions_map, "Regions")

    # in the color image, paint with green the areas which belong to a plant
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

    # Show which regions are classified as a plant
    visualize(new_list, "Is plant")

    # Show color image in the background
    cv2.imshow("Is Plant", new_col_im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()
