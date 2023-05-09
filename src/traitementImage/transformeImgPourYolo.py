"""
programme qui prend en entrée le chemin vers une image et applique les transformation pour yolo
l'image prete est écrite sous le nom <nomPhoto>OK.png
"""



import os
import sys
import cv2 as cv
from TraitementImage import *


# if len(sys.argv) == 1 or len(sys.argv) > 4:
# 	print("Usage : prog.py CheminVersPhoto [typeBinarisation [Seuil]]")
# 	exit()

# if len(sys.argv) == 2:
# 	cheminPhoto = sys.argv[1]





# on commence les transformations
def transformePourYolo(img, typeBinarisation=0, Seuil=128):
	# la photo est la photo prise par l'appareil photo (en couleur, n'importe quelle résolution etc)
	img = cv.cvtColor(img,cv.COLOR_BGR2GRAY) # nvDeGris

	# if len(sys.argv) == 3:
	# 	img = binarisation(img, sys.argv[2])
	# elif len(sys.argv) == 4:
	# 	img = binarisation(img, sys.argv[2], sys.argv[3])
	# else:
	# 	img = binarisation(img)
	# # l'image est binarisée

	img = binarisation(img, typeBinarisation, Seuil)

	# on applique la dilation
	img = dilateCommeIlFaut(img)

	# une fois que la lettre "ressemble" à une lettre de la bdd train de yolo, on redimensionne en 128
	img = redimensionneImageEn128SansBord(img)

	return img
	



try: 
	os.mkdir("pretPourYolo") # le dossier n'existe pas
except OSError as error: 
	
	#le dossier existe déjà, on détruit les fichiers
	for filename in os.listdir("pretPourYolo"):
		os.remove("pretPourYolo/" + filename)


for filename in os.listdir("imageSegmentee"):
	imgSegmentee = cv.imread("imageSegmentee/"+filename)
	imgPrete = transformePourYolo(imgSegmentee)
	cv.imwrite("pretPourYolo/" + filename[0:-4] + "OK.png", imgPrete)






