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
	MAXCLICKFRAME = 16
	COL_CLICK = (255,255,255,255)
	img = pygame.image.load('input.png')
	backgroundimage = img
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
	
	print "Window resolution: "
	print height,width
	
	numrows = int(height/TILESIZE)
	numcols = int(width/TILESIZE)
	
	C = choosePalette()
	(r,g,b) = C[0]
	(r1,g1,b1) = (255,255,0)
	name = "Planet X"
	thePlanet = Planet(name, 1.0, 0, (r,g,b,255), (r1,g1,b1,255))

	PLANETS.append((thePlanet, (0,0), name, TILESIZE/(randint(3,7)), pi*2.0/720 ))
	
	MISSILES = [] # All the moving things
	CLICKANIM = [] # Animated places where the player has clicked
	
	lastclickloc = (0,0)

	scorefont = pygame.font.SysFont("monospace", 15)
	playerScore = 0
	
	wavecount = 1
	wavelength = 200 # frames
	wavepos = 0
	wavestep = pi/2.0/float(wavelength)
	print wavecount,wavelength,wavepos,wavestep
	while True: # main game loop
		mouseClicked = False
		iterationCount = iterationCount+1
		if iterationCount%100 == 0: # Cleanup
			MLIST = []
			for (a,b,c) in MISSILES:
				# print "Collecting garbage "+str(len(MISSILES))
				if a.alive == True:
					MLIST.append((a,b,c))
				if len(MLIST) > 0:
					MISSILES = MLIST
		NEWMISSILES = []
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
					CLICKANIM.append((px,py,MAXCLICKFRAME))
					lx,ly = lastclickloc
					dx = px-lx
					dy = py-ly
					if (dx**2+dy**2) > 4: # Suppress spam clicking in the same spot
						lastclickloc = (px,py)

						for (missile,missileobj,mr) in MISSILES:
							if missile.alive == True:
								(mx,my) = missile.position
								mr = missileobj.radiusAvg
								#check if the distance between the objects is less than the combined radius
								dx = px-mx
								dy = py-my
								distance = sqrt(dx**2+dy**2)

								if distance < mr*2 or distance < MAXCLICKFRAME: # Kludgy
									angle = atan2(dy,dx)
									# print missile.name+" destroyed "
									missile.alive = False
									playerScore = playerScore+mr
									
									if mr > 10 and len(MISSILES) < 100:
										# print missile.name+" fragmented "
										(ang,speed) = missile.velocity
										newDir = random()*2.0*pi
										NUMFRAGS = randint(2,12)
										dang = pi*2.0/NUMFRAGS
										for i in xrange(0,NUMFRAGS):
											newMissile = Missile("Fragment",(mx,my),(newDir+dang+dang/3*randint(-1,1),speed/randint(1,5)))
											newMissileObj = Planet(name, 0.1, randint(1,15)*pi/360, (192,148,92,255), (100,100,0,255))
											NEWMISSILES.append((newMissile,newMissileObj,int(mr)>>1))
											dang = dang+dang
										
					
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
					missileObj = Planet(name, 0.1, randint(1,15)*pi/360, (192,148,92,255), (100,100,0,255))
					MISSILES.append((missile,missileObj,randint(30,300)))

					mouseClicked = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					print "Key press: "+str(event.key)

		# Draw
		#surface.fill(COL_CANVAS)
		surface.blit(backgroundimage,[0,0])
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
		
		NEWCLICKANIM = []
		for (x,y,frame) in CLICKANIM:
			# print x,y,frame
			if frame > 0:
				frame = frame - 1
				for i in xrange(-frame,frame+1):
					
					pixels[x+i][y-frame] = COL_CLICK
					pixels[x+i][y+frame] = COL_CLICK
					pixels[x+frame][y+i] = COL_CLICK
					pixels[x-frame][y+i] = COL_CLICK
				NEWCLICKANIM.append((x,y,frame))
		CLICKANIM = NEWCLICKANIM
		
		del pixels
		# Overlays and labels
		(ox,oy) = centre
		
		# Display the score
		scorelabel = scorefont.render(str(int(playerScore)) , 1, (255,190,120))
		wavelabel = scorefont.render("W."+str(int(wavecount)) , 1, (128,190,255))
		
		slw = scorelabel.get_width()
		slh = scorelabel.get_height()

		surface.blit(scorelabel, (ox-(slw>>1), oy-(slh>>1)))
		surface.blit(wavelabel, (ox-(slw>>1), oy-(slh>>1)+10))
		pygame.display.update()
					
		# Other Simulation updates
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
						# print name+" has collided with "+missile.name+" at "+str(angle)
						missile.alive = False

						thePlanet.impacts.append((angle-thePlanet.rotation,mr,missile.velocity)) # An object of radius mr has impacted at angle
					# print (px,py,pr,mx,my,mr)
			thePlanet.impactsHandler() # Process impacts
			for (newMissile,newMissileObj,sz) in thePlanet.debris:
				(mx,my) = newMissile.position
				newMissile.position = (int(mx*scale)+(width>>1),int(my*scale)+(height>>1))
				MISSILES.append((newMissile,newMissileObj,sz))
			thePlanet.debris = []
		for missile in NEWMISSILES:
			MISSILES.append(missile)
		
		# Enemy wave logic (Temporary)
		if iterationCount%wavelength == 0:
			wavecount = wavecount +1
		wavepos = wavepos+wavestep
		if wavepos > pi*2.0:
			wavepos = 0
		if 10.0*random() < sin(wavepos): # Spawn a new asteroid
			radius = (width>>1)+width
			# print radius
			angle = random()*pi*2.0

			NUMFRAGS = (wavecount>>1)+1
			for i in xrange(0,NUMFRAGS):
				newDir = angle+pi+randint(-2,2)*pi/720
				speed = randint(5,20)
				name = "Wave Chunk"
				newMissile = Missile(name,(ox + radius*cos(angle),oy + radius*sin(angle)),(newDir,speed/randint(1,5)))
				newMissileObj = Planet(name, 0.1, randint(1,15)*pi/360, (255,148,92,255), (100,100,0,255))
				MISSILES.append((newMissile,newMissileObj,randint(30,300)))

			

doit()