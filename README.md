# REDUCE COLORS
Progetto che permette di semplificare un'immagine riconducendo ogni colore
a quello più simile tra quelli dati.

#INSTALLAZIONE
Requisiti:
* python 2.7
* moduli python:
	* cv2
	* numpy
	* colormath

# STRUTTURA
La directory principale contiene:
* un file "main.py" che se eseguito mostra un esempio di funzionamento del progetto.
* un file "conversion.py" che contiene le funzioni necessarie per la semplificazione
  dei colori di un'immagine.
* un file "colors.txt" in cui è possibile scrivere in formato RGB i colori in cui si vuole
  che l'immagine venga semplificata
* una cartella "images/" in cui sono presenti alcune immagini utilizzabili per mostrare un
  esempio di funzionamento del programma.
* Le immagini elaborate verranno messe in una cartella "results/".

# ESEMPIO DI USO
Risultato del comando "python main.py --help":

usage: main.py [-h] -i IMAGE [-f FILE] [-m MODE]

Riduzione di un'immagine in N colori

optional arguments:
  -h, --help            show this help message and exit

  -i IMAGE, --image IMAGE Immagine di input

  -f FILE, --file FILE  File con i colori da estrapolare

  -m MODE, --mode MODE  Modalità di conversione: i valori possibili sono:

			* 0 per la conversione utilizzando l'algoritmo DELTA E CIE2000.

			* 1 per la conversione riconducendo ogni colore a quello più vicino
			  nello spazio RGB.

			* 2 per la conversione riconducendo ogni colore a quello più
                          vicino nello spazio HSV.
													
