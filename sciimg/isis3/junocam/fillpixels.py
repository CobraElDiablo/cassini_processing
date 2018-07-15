import sys
import os
import numpy as np
from libtiff import TIFFimage
from PIL import Image
from corrections import DEAD_PIXEL_MAP

BAND_HEIGHT = 128


def linear_interpolate(v0, v1, f):
    v = (v0 * f) + (v1 * (1.0 - f))
    return v


def open_image(img_path):
    img = Image.open(img_path)
    data = np.copy(np.asarray(img))
    img.close()

    return data

def fill_dead_pixel(data, band_num, band_id, band_height=BAND_HEIGHT):

    dead_pixels = DEAD_PIXEL_MAP[band_id]

    top = band_num * band_height
    bottom = top + band_height

    for dead_pixel in dead_pixels:
        cx = dead_pixel[0]
        cy = dead_pixel[1] + top
        radius = dead_pixel[2]

        for y in range(-radius, radius):
            for x in range(-radius, radius):
                x0 = data[cy + y][cx - radius]
                x1 = data[cy + y][cx + radius]
                y0 = data[cy - radius][cx + x]
                y1 = data[cy + radius][cx + x]

                fx = ((x + radius) / (radius*2.0))
                fy = ((y + radius) / (radius*2.0))

                ix = linear_interpolate(x0, x1, fx)
                iy = linear_interpolate(y0, y1, fy)

                v = np.mean([ix, iy])

                data[cy + y][cx + x] = v


def fillpixels(img_data, verbose=False):
    img_height = img_data.shape[0]

    if verbose:
        print "Image height:", img_height

    bands_per_image = (img_height / BAND_HEIGHT / 3)

    if verbose:
        print "Detected", bands_per_image, "RGB bands"

    for band in range(0, bands_per_image):
        if verbose:
            print "Filling pixels for RGB band triplet #", band
        fill_dead_pixel(img_data, band * 3 + 0, 0, band_height=BAND_HEIGHT)
        fill_dead_pixel(img_data, band * 3 + 1, 1, band_height=BAND_HEIGHT)
        fill_dead_pixel(img_data, band * 3 + 2, 2, band_height=BAND_HEIGHT)



def process_image(img_path, save_file_path=None, verbose=False):

    if verbose:
        print "Filling dead pixels in", img_path

    data = open_image(img_path)

    fillpixels(data, verbose=verbose)

    if save_file_path is None:
        save_file_path = "%s-filled.tif" % (img_path[0:-4])

    if verbose:
        print "Saving processed data to", save_file_path

    tiff = TIFFimage(data, description='')
    tiff.write_file(save_file_path, compression='none', verbose=False)

    return save_file_path


# For testing
if __name__ == "__main__":

    img_path = sys.argv[1]
    process_image(img_path, verbose=True)