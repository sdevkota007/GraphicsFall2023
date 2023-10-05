import pygame as pg

def load_image(filename):
    img = pg.image.load(filename)
    img_data = pg.image.tobytes(img, "RGB", True)
    w, h = img.get_size()
    return img_data, w, h