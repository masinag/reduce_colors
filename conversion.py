### -*- coding: utf-8 -*-
from cv2 import imread, imwrite, imshow, waitKey, destroyAllWindows, cvtColor, \
COLOR_BGR2RGB, COLOR_RGB2BGR, COLOR_BGR2HSV, COLOR_HSV2BGR, COLOR_RGB2HSV, \
COLOR_BGR2LAB, COLOR_LAB2BGR, COLOR_RGB2LAB
from numpy import array, zeros, uint8, array_equal, sqrt, power
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from time import time
# from imutils import resize
from argparse import ArgumentTypeError

# modalità in cui è possibile semplificare un'immagine
MODE_DELTAECIE2000 = 0
MODE_RGB = 1
MODE_HSV = 2

def modes(mode):
    mode = int(mode)
    if not mode in [MODE_DELTAECIE2000, MODE_RGB, MODE_HSV]:
        raise argparse.ArgumentTypeError("%s " % n)
    return mode

def read_colors(file):
    s = list()
    with open(file) as f:
        for r in f:
            rr = r.replace("\n", "")
            s.append(rr.split(","))
    return s
def _get_value(pixel):
    """Restituisce un intero in base 10 a partire da un pixel dato."""
    return pixel.item(0)*65536 + pixel.item(1)*256 + pixel.item(2)
#
# def distance_LAB2(p1, p2):
#     """Restituisce un valore indicante la differenza tra 2 pixel in formato LAB.
#     La differenza viene calcolata con l'algoritmi DELTA E CIE2000."""
#     # converto i colori in formato LAB
#     p2 = LabColor(p2.item(0)/255.0, p2.item(1)/255.0, p2.item(2)/255.0)
#     p1 = LabColor(p1.item(0)/255.0, p1.item(1)/255.0, p1.item(2)/255.0)
#     # e calcolo la differenza
#     return delta000_e_cie2000(p1, p2)

def distance_DELTAECIE2000(p1, p2):
    """Restituisce un valore indicante la differenza tra 2 pixel in formato RGB.
    La differenza viene calcolata con l'algoritmi DELTA E CIE2000."""
    # converto i colori in formato LAB
    p1 = convert_color(sRGBColor(p1.item(0)/255.0, p1.item(1)/255.0, p1.item(2)/255.0), LabColor)
    p2 = convert_color(sRGBColor(p2.item(0)/255.0, p2.item(1)/255.0, p2.item(2)/255.0), LabColor)
    # e calcolo la differenza
    return delta_e_cie2000(p1, p2)

def distance_RGB(p1, p2):
    """Restituisce un valore indicante la differenza tra 2 pixel in formato RGB.
    La differenza viene calcolata come la semplice distanza tra i colori in
    formato RGB."""
    (r1,g1,b1) = p1
    (r2,g2,b2) = p2
    return sqrt(power(int(r1) - int(r2),2) + power(int(g1) - int(g2), 2) + power(int(b1) - int(b2), 2))

def distance_HSV(p1, p2):
    """Restituisce un valore indicante la differenza tra 2 pixel in formato HSV.
    La differenza viene calcolata come la semplice distanza tra i colori in
    formato HSV."""
    (h1,s1,v1) = p1
    (h2,s2,v2) = p2
    return sqrt(power(int(h1) - int(h2),2) + power(int(s1) - int(s2), 2) + power(int(v1) - int(v2), 2))
    # return sqrt(power(int(h1) - int(h2),2) + power(int(v1) - int(v2), 2))

def closer_color(pixel, colors, distance_function):
    """Restituisce il colore piu vicino al pixel. I colori vengono confrontati
    utilizzando la funzione passata come parametro."""
    # cerco il colore con la differenza minore dal colore del pixel
    min_diff = distance_function(pixel, colors[0])
    closer_color = colors[0]
    for color in colors[1:]:
        d = distance_function(pixel, color)
        if d < min_diff:
            min_diff = d
            closer_color = color
    return closer_color

def convert(image, colors, distance_function):
    """Converte un'immagine nei colori passati come parametro, sostituendo ad
    ogni pixel uno del colore più vicino tra quelli dati. La distanza viene
    calcolata utilizzando la funzione passata come parametro"""
    met_colors = {_get_value(c):c for c in colors}
    # "prendo" larghezza e altezza
    (h, w) = image.shape[:2]
    # creo la nuova immagine che sarà quella convertita
    mod_image = zeros((h, w, 3), uint8)
    # scorro i pixel dell'immagine
    for i in xrange(h):
        for j in xrange(w):
            # trovo il pixel (uso i metodi degli array di numpy che sono più veloci)
            pixel = array([image.item(i, j, 0), image.item(i, j, 1), image.item(i, j, 2)], uint8)
            # se il colore non è già tra quelli in cui devo convertire l'immagine,
            # trovo quello più vicino
            value = _get_value(pixel)
            try:
                pixel = met_colors[value]
            except KeyError as e:
                pixel = closer_color(pixel, colors, distance_function)
                met_colors[value] = pixel
            # scrivo il colore sulla nuova immagine
            mod_image.itemset((i, j, 0), pixel.item(0))
            mod_image.itemset((i, j, 1), pixel.item(1))
            mod_image.itemset((i, j, 2), pixel.item(2))
    return mod_image

# def simplify_image_LAB2(image, colors):
#     # converto colori e immagine in RGB
#     # image = resize(image, width = 300)
#     image = cvtColor(image, COLOR_BGR2LAB)
#     conv_colors = [cvtColor(array([[c]]), COLOR_RGB2LAB)[0][0] for c in colors]
#     mod_image = convert(image, conv_colors, distance_LAB2)
#     return cvtColor(mod_image, COLOR_LAB2BGR)

def simplify_image_LAB(image, colors):
    """'Semplifica' un'immagine con i colori passati come parametro. I colori
    vengono confrontati utilizzando l'algoritmo delta e 2000."""
    # converto colori e immagine in RGB
    # image = resize(image, width = 300)
    image = cvtColor(image, COLOR_BGR2RGB)
    mod_image = convert(image, colors, distance_DELTAECIE2000)
    return cvtColor(mod_image, COLOR_RGB2BGR)

def simplify_image_RGB(image, colors):
    """'Semplifica' un'immagine con i colori passati come parametro. I colori
    vengono confrontati tramite la distanza nello spazio RGB."""
    image = cvtColor(image, COLOR_BGR2RGB)
    mod_image = convert(image, colors, distance_RGB)
    return cvtColor(mod_image, COLOR_RGB2BGR)

def simplify_image_HSV(image, colors):
    """'Semplifica' un'immagine con i colori passati come parametro. I colori
    vengono confrontati tramite la distanza nello spazio HSV."""
    # converto colori e immagine in HSV
    conv_colors = [cvtColor(array([[c]]), COLOR_RGB2HSV)[0][0] for c in colors]
    image = cvtColor(image, COLOR_BGR2HSV)
    mod_image = convert(image, conv_colors, distance_HSV)
    return cvtColor(mod_image, COLOR_HSV2BGR)

def simplify_image(image, colors, mode = MODE_HSV):
    """Legge un'immagine e la 'semplifica' un'immagine con i colori passati come
    parametro. La modalità di confronto di default è la distanza nello spazio
    HSV ma può essere modificata tramite il parametro mode."""

    image = imread(image)

    if mode == MODE_DELTAECIE2000:
        return simplify_image_LAB(image, colors)
    elif mode == MODE_RGB:
        return simplify_image_RGB(image, colors)
    elif mode == MODE_HSV:
        return simplify_image_HSV(image, colors)
    else:
        return False
