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
from Missile import Missile

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
	
#	for x in xrange(0,numcols):
#		for y in xrange(0,numrows):
	C = choosePalette()
	(r,g,b) = C[0]
	(r1,g1,b1) = (255,255,0)
	name = "Planet X"
	thePlanet = Planet(name, 1.0, 0, (r,g,b,255), (r1,g1,b1,255))

	#for i in xrange(0,randint(256,256)):
	#	objheight = randint(1,4)*3
	#	objwidth = 2
	#	thePlanet.addSurfaceFeature(random()*pi*2.0, "Building", "Skyscraper", 
	#	[
	#	(0,-objwidth),(0,-objwidth),
	#	(objheight,-objwidth),(objheight,-objwidth),
	#	(objheight,objwidth),(objheight,objwidth),
	#	(0,objwidth),(0,objwidth),
	#	])
	
	PLANETS.append((thePlanet, (0,0), name, TILESIZE/(randint(3,7)), pi*2.0/720 ))
	
	
#	thePlanet = Planet("The Planet", (255,210,192,255), (255,255,0,255))
#	planetscale = width>>2
#	planetrotatedelta = pi*2.0/360
	
	MISSILES = []
	
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
				if event.button == LEFT: # Have we clicked on an asteroid?
					(px,py) = event.pos
					for (missile,missileobj,mr) in MISSILES:
						if missile.alive == True:
							(mx,my) = missile.position
							mr = missileobj.radiusAvg
							#check if the distance between the objects is less than the combined radius
							dx = px-mx
							dy = py-my
							distance = sqrt(dx**2+dy**2)

							if distance < mr:
								angle = atan2(dy,dx)
								print missile.name+" destroyed "
								missile.alive = False
								
								if mr > 20:
									print missile.name+" fragmented "
									(ang,speed) = missile.velocity
									newMissile = Missile("Chunk",(mousex,mousey),speed/2)
									newMissileObj = Planet(name, 0.1, randint(1,15)*pi/360, (192,148,92,255), (100,100,0,255))
									MISSILES.append((newMissile,newMissileObj,int(mr)>>1))
									newMissile = Missile("Chunk",(mousex,mousey),speed/2)
									newMissileObj = Planet(name, 0.1, randint(1,15)*pi/360, (192,148,92,255), (100,100,0,255))
									MISSILES.append((newMissile,newMissileObj,int(mr)>>1))				
				
  					mouseClicked = True
				elif event.button == RIGHT: # Create a new asteroid
					mousex, mousey = event.pos
					(x,y) = event.pos
					dx = x-ox
					dy = y-oy
					direction = atan2(dy,dx)+pi
					distance = sqrt(dx**2+dy**2)
					if distance > 0:
						speed = 5.0*random() #1.0/distance

					missile = Missile("Chunk",(mousex,mousey),(random()*2.0*pi,speed))
					missileObj = Planet(name, 0.1, randint(1,15)*pi/90, (192,148,92,255), (100,100,0,255))
					MISSILES.append((missile,missileObj,randint(30,300)))

					mouseClicked = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					print "Key press: "+str(event.key)

		# Draw
		surface.fill(COL_CANVAS)
#		thePlanet.draw(surface,centre,planetscale)
		for ((thePlanet, (x,y), name, scale, rotationdelta )) in PLANETS:
			# print x,y
			if len(thePlanet.surfacefeatures) < 100 and iterationCount%100 == 0: # Add a new building randomly at interval
				objheight = randint(1,4)*3
				objwidth = 2
				thePlanet.addSurfaceFeature(random()*pi*2.0, "Building", "Skyscraper", 
				[
				(0,-objwidth),(0,-objwidth),
				(objheight,-objwidth),(objheight,-objwidth),
				(objheight,objwidth),(objheight,objwidth),
				(0,objwidth),(0,objwidth),
				])				
			
			# thePlanet.rotate(rotationdelta)
			thePlanet.draw(surface,(width>>1,height>>1),scale)

		pixels = pygame.PixelArray(surface)
		for x in xrange(0,numcols):
			for y in xrange(0,numrows):
				pixels[x*TILESIZE][y*TILESIZE] = (128,128,128,255)

		for (missile,missileobj,radius) in MISSILES:
			if missile.alive == True:
				(x,y) = missile.position
				if x > -width and x < width<<1 and y > -height and y < height<<1: # only draw within a local area
					missileobj.draw(surface,missile.position,radius)
		pygame.display.update()
		
		# Other Simulation updates
		(ox,oy) = centre
		for (missile,missileobj,radius) in MISSILES:
			if missile.alive == True:
				missile.move()
				
				# Acceleration toward centre of the planet...
				(x,y) = missile.position
				dx = x-ox
				dy = y-oy
				direction = atan2(dy,dx)+pi
				distance = sqrt(dx**2+dy**2)
				if distance > 0:
					speed = 10.0*1.0/distance
					missile.accelerate(direction,speed)

		# Check for, and handle, collisions
		# For each planet, is there an asteroid colliding?
		ox,oy = centre
		for ((thePlanet, (px,py), name, scale, rotationdelta )) in PLANETS:
			pr = thePlanet.radiusAvg
			px = px + ox
			py = py + oy
			for (missile,missileobj,mr) in MISSILES:
				if missile.alive == True:
					(mx,my) = missile.position
					mr = missileobj.radiusAvg
					#check if the distance between the objects is less than the combined radius
					dx = px-mx
					dy = py-my
					distance = sqrt(dx**2+dy**2)

					if distance < pr+mr:
						angle = atan2(dy,dx)
						print name+" has collided with "+missile.name+" at "+str(angle)
						missile.alive = False

						thePlanet.impacts.append((angle-thePlanet.rotation,mr,missile.velocity)) # An object of radius mr has impacted at angle
					# print (px,py,pr,mx,my,mr)
			thePlanet.impactsHandler() # Process impacts
				
doit()