"""  
fonctions utiles pour transformer une image en quelque chose d'utile pour YOLO

les fonctions prennent une image en entrée, elle doit être binarisée et en niveau de gris
(voir fonction  cv.cvtColor(img, cv.COLOR_BGR2GRAY)  

"""



#assert <img> is not None,  "Message qui dit que ça a pas marché"

import cv2 as cv
import os


SEUIL_BASIQUE = 0
SEUIL_ADAPTATIF = 1
SEUIL_ADAPTATIF_GAUSSIEN = 2
SEUIL_OTSU = 3
SEUIL_OTSU_GAUSS = 4



def binarisation(imgIn, typeBinarisation = 0, Seuil=10):
	match typeBinarisation:
		case 0 :#SEUIL_BASIQUE:
			_, img = cv.threshold(imgIn, Seuil, 255, cv.THRESH_BINARY)
		
		case 1 :#SEUIL_ADAPTATIF:
			img = cv.adaptiveThreshold(imgIn, 255 , cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11 , 2) 
		
		case 2 :#SEUIL_ADAPTATIF_GAUSSIEN:
			img = cv.adaptiveThreshold(imgIn, 255 , cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11 , 2)
		
		case 3 :#SEUIL_OTSU:
			_, img = cv.threshold(imgIn, Seuil ,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
		
		case 4 :#SEUIL_OTSU_GAUSS:
			blur = cv.GaussianBlur(imgIn,(5,5),0)
			_, imgOtsuGauss = cv.threshold(blur, Seuil ,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
		
		case _:
			print("mauvais argument pour typeBinarisation, aucun seuillage appliqué")
	
	return img
	


def ouverture(imgIn):
    imgOut = imgIn.copy()
    kernel_open = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
    imgOut = cv.dilate(imgOut, kernel_open)
    return imgOut



def fermeture (imgIn):
    imgOut = imgIn.copy()
    kernel_close = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
    imgOut = cv.erode(imgOut, kernel_close)
    return imgOut



def compteNbFermeture(imgIn):

	img = cv.bitwise_not(imgIn) #on inverse prck faut compter le nombre de pixels noir, pas blanc
	
	compteurNbFermeture = 0
	while cv.countNonZero(img) != 0:
		img = fermeture(img)
		compteurNbFermeture += 1
	
	return compteurNbFermeture



def dilateCommeIlFaut(img):
	""" 
	dilate (ou rétrécit) le bon nombre de fois pour que YOLO arrive mieux à deviner
	il faut que l'image entrée soit binarisée
	"""

	nbFermetureAFaire = 8 - compteNbFermeture(img)
	# 9 correspond en gros à l'épaisseur des images utilisée pour entrainer YOLO

	if nbFermetureAFaire < 0: # le trait est trop épais, on augmente le blanc ( et réduit le noir, i.e. la lettre)
		for i in range(-1 * nbFermetureAFaire):
			img=ouverture(img)  
	else:
		for i in range(nbFermetureAFaire): # le trait est pas assez épais, on réduit le blanc (et on dilate le noir, i.e. la lettre)
			img=fermeture(img) 
	
	return img


def redimensionneImageEn128SansBord(imgIn):
	""" rogne l'image en supprimant les bandes blanches du bord de l'image,
		et redimensionne l'image en 128x128, en respectant à peu près l'échelle
		(l'image est normalement binarisée)
		"""
	
	img = cv.bitwise_not(imgIn) #on inverse prck pour opencv le fond est noir et l'objet est blanc
	x,y,w,h = cv.boundingRect(img) # on prend le rectangle de la zone d'intéret
	img = img[y:y+h, x:x+w]  # on crop
	imgAvantResize = cv.bitwise_not(img) #on reinverse pour avoir la lettre en noir (c'est + beau)

	img = cv.resize(imgAvantResize, (128,128), interpolation = cv.INTER_NEAREST_EXACT ) #on resize comme il faut en 128
	#INTER_NEAREST_EXACT est la meilleure interpolation qu'on ait testée (floute pas et respecte bien l'échelle)

	_, img = cv.threshold(img, 10, 255, cv.THRESH_BINARY) # on seuil prck ptre que ça floute de resize

	return img
