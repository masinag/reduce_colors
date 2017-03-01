### -*- coding: utf-8 -*-

if __name__ == '__main__':
    from argparse import ArgumentParser
    from numpy import array, uint8
    from conversion import simplify_image, MODE_DELTAECIE2000, MODE_RGB, MODE_HSV, modes
    from time import time
    from cv2 import imwrite
    from os.path import exists, basename
    from os import makedirs


    parser = ArgumentParser(description = "Riduzione di un'immagine in N colori")
    parser.add_argument("-i", "--image", type = str, required = True, help="Immagine di input")
    parser.add_argument('-f', '--file', type=str, help="File con i colori da estrapolare")
    parser.add_argument("-m", "--mode", type = modes, default = MODE_HSV,
    help="""
        Modalità di conversione: i valori possibili sono:
	* 0 per la conversione utilizzando l'algoritmo DELTA E CIE2000.
	* 1 per la conversione riconducendo ogni colore a quello più vicino nello spazio RGB.
	* 2 per la conversione riconducendo ogni colore a quello più vicino nello spazio HSV.
    """)
    # parser.add_argument('-r', '--resize', type=int, help = "Ridimesionamento dell'immagine")

    args = parser.parse_args()

    colors = array([[255,  0,  0], #red
                    [  0,255,  0], #green
                    [  0,  0,255], #blue
                    [255,255,255], #white
                    [  0,  0,  0]],# black
                    uint8)

    clean_name, extension = basename(args.image).split(".")
    if not exists("results"):
        makedirs("results")
    if not exists("results/%s" % clean_name):
        makedirs("results/%s" % clean_name)

    names = {0:"deltaecie2000", 1:"rgb", 2:"hsv"}
    im = simplify_image(args.image, colors, args.mode)
    if im is False:
        print "%d non è una modalità valida" % value
    else:
	imwrite("results/%s/%s_%s.%s" %(clean_name, clean_name, names[args.mode], extension), im)
