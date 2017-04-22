# @abrightmoore

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import randint, random, Random
from os import listdir
from os.path import isfile, join
from copy import deepcopy
import glob
import inspect
import pygame, sys
from pygame.locals import *
from io import BytesIO
import imageio
from numpy import *

from Colours import *
from ImageTools import *
from Planet import Planet

#import Palette # @abrightmoore
pygame.init()

def choosePalette():
	# Choose a palette
	C = []
	chance = randint(1,10)
	if chance == 1:
		C = getRandomAnalogousColours()
	elif chance == 2:
		C = getRandomComplementaryColours()
	else:
		C = getColoursBrownian(randint(16,64),randint(4,16))
	# Palette chosen
	return C

def doit():
	print "By @abrightmoore."
	FPS = 120
	COL_CANVAS = (0,0,0,0)
	LEFT = 1 # Mouse event
	RIGHT = 3 # Mouse event
	
	img = pygame.image.load('input.png')
	width = img.get_width()
	height = img.get_height()
	centre = (width>>1,height>>1)

	surface = pygame.display.set_mode((width, height)) # A copy of the source image in size
	surface.fill(COL_CANVAS) # Parchment colour to the canvas
	pygame.display.set_caption('Blow Up Planets')
	mousex = 0
	mousey = 0
	fpsClock = pygame.time.Clock()
	fpsClock.tick(FPS)
	iterationCount = 0

	PLANETS = []
	TILESIZE = 600
	
	print height,width
	
	numrows = int(height/TILESIZE)
	numcols = int(width/TILESIZE)
	
	for x in xrange(0,numcols):
		for y in xrange(0,numrows):
			C = choosePalette()
			(r,g,b) = C[0]
			(r1,g1,b1) = (255,255,0)
			name = "Planet "+str(x+numrows*y)
			thePlanet = Planet(name, (r,g,b,255), (r1,g1,b1,255))

			for i in xrange(0,randint(64,256)):
				objheight = randint(1,5)*5
				objwidth = 2
				thePlanet.addSurfaceFeature(random()*pi*2.0, "Building", "Skyscraper", 
				[
				(0,-objwidth),(0,-objwidth),
				(objheight,-objwidth),(objheight,-objwidth),
				(objheight,objwidth),(objheight,objwidth),
				(0,objwidth),(0,objwidth),
				])
			
			PLANETS.append((thePlanet, (x*TILESIZE,y*TILESIZE), name, TILESIZE/(randint(3,7)), pi*2.0/randint(360,720)*randint(-1,1) ))
	
	
#	thePlanet = Planet("The Planet", (255,210,192,255), (255,255,0,255))
#	planetscale = width>>2
#	planetrotatedelta = pi*2.0/360
	
	while True: # main game loop
		mouseClicked = False
		iterationCount = iterationCount+1

		# Input
		for event in pygame.event.get():
			if event.type == QUIT:
				print "Shutting down."
				pygame.quit()
				sys.exit()	
			elif event.type == MOUSEMOTION:
 				mousex, mousey = event.pos
 			elif event.type == MOUSEBUTTONUP:
				if event.button == LEFT:
 					mousex, mousey = event.pos
 					mouseClicked = True
				elif event.button == RIGHT:
					mouseClicked = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					print "Key press: "+str(event.key)

		# Draw
		surface.fill(COL_CANVAS)
#		thePlanet.draw(surface,centre,planetscale)
		for ((thePlanet, (x,y), name, scale, rotationdelta )) in PLANETS:
			# print x,y
			thePlanet.rotate(rotationdelta)
			thePlanet.draw(surface,(x+(TILESIZE>>1),y+(TILESIZE>>1)),scale)
		pixels = pygame.PixelArray(surface)
		for x in xrange(0,numcols):
			for y in xrange(0,numrows):
				pixels[x*TILESIZE][y*TILESIZE] = (128,128,128,255)
		
		pygame.display.update()
		
		# Other Simulation updates
		
doit()