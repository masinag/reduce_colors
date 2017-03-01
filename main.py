### -*- coding: utf-8 -*-

if __name__ == '__main__':
    from argparse import ArgumentParser
    from numpy import array, uint8
    from conversion import simplify_image, MODE_DELTAECIE2000, MODE_RGB, MODE_HSV
    from time import time
    from cv2 import imwrite
    from os.path import exists
    from os import makedirs


    parser = ArgumentParser(description = "Riduzione di un'immagine in N colori")
    parser.add_argument("-i", "--image", type = str, required = True, help="Immagine di input")
    parser.add_argument('-f', '--file', type=str, help="File con i colori da estrapolare")
    parser.add_argument("-m", "--mode", type = conversion.modes, default = MODE_HSV,
    help="""
        Modalità di conversione: i valori possibili sono 0, 1 o 2
    """)
    # parser.add_argument('-r', '--resize', type=int, help = "Ridimesionamento dell'immagine")

    args = parser.parse_args()

    colors = array([[255,  0,  0], #red
                    [  0,255,  0], #green
                    [  0,  0,255], #blue
                    [255,255,255], #white
                    [  0,  0,  0]],# black
                    uint8)

    clean_name, extension = args.image.split(".")
    if not exists("results"):
        makedirs("results")
    if not exists("results/%s" % clean_name):
        makedirs("results/%s" % clean_name)

    # provo a semplificare l'immagine in divese modalità
    modes = {"delta_e_cie2000" : MODE_DELTAECIE2000,
             "rgb" : MODE_RGB,
             "hsv" : MODE_HSV}

    # modes = {"hsv" : MODE_HSV}

    for key, value in modes.items():
        t = time()
        im = simplify_image(args.image, colors, value)
        if im is False:
            print "%d non è una modalità valida" % value
        else:
            imwrite("results/%s/%s_%s.%s" %(clean_name, clean_name, key, extension), im)
            print "%s Fatto" % key
            print "Tempo: %.3f" % (time() - t)
