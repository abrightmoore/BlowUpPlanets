# @abrightmoore
#
# A planet has a surface, a core, and various surface features
# It can be deformed
# It can be rendered

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import randint, random, Random
from os import listdir
from os.path import isfile, join
from copy import deepcopy
import glob
import inspect
from io import BytesIO
import imageio
import pygame, sys
from pygame.locals import *
#from numpy import *

from Lines import *

class Planet:
	# Class variables shared by all instances go here
	SMOOTHAMOUNT = 3 # How many times to run Chaiken across the points
	TWOPI = pi*2.0
	# End Class variables
	
	def __init__(self, name, colcrust, colcore):
		# Instance variables unique to each instance go here
		self.name = name # Label the planet for easy reference later
		segments = 40 # initial number of sections around the circumference
		crustradius = 1.0
		coreradius = crustradius / 3.0
		self.colcrust = colcrust
		self.colcore = colcore
		self.rotation = random()*pi*2.0
		self.crust = []
		self.core = []
		for i in xrange(0,segments):
			self.crust.append((crustradius+randint(0,5)*0.01)) # ToDo: Add height variation
			self.core.append((coreradius+randint(0,10)*0.01)) # ToDo: Add height variation
	
		self.surfacefeatures = []
	
	def addSurfaceFeature(self, angle, type, name, points):
		self.surfacefeatures.append((angle,type,name,points))
	
	def rotate(self,angle):
		self.rotation = self.rotation + angle
		if self.rotation > pi:
			self.rotation = self.rotation-self.TWOPI
		if self.rotation < pi:
			self.rotation = self.rotation+self.TWOPI
	
	def draw(self,surface,centre,scale):
		width = surface.get_width()
		height = surface.get_height()
		(ox,oy) = centre # View port co-ordinates to centre the planet on.
		#print centre
		
		P = [] # Points to interpolate with Chaikin
		count = 0
		angledelta = pi*2.0/len(self.core)
		for (r) in self.core:
			a = count*angledelta+self.rotation
			x = scale*r*cos(a)
			y = scale*r*sin(a)
			P.append((x+ox,y+oy,0)) # ToDo: Utilise z. Currently ignored
			count = count+1
		P.append(P[0])
		P.append(P[1])
		COREPIX = calcLinesSmooth(self.SMOOTHAMOUNT,P) # Creates a smooth line

		P = [] # Points to interpolate with Chaikin
		count = 0
		angledelta = pi*2.0/len(self.crust)
		for (r) in self.crust:
			a = count*angledelta+self.rotation
			x = scale*r*cos(a)
			y = scale*r*sin(a)
			P.append((x+ox,y+oy,0)) # ToDo: Utilise z. Currently ignored
			count = count+1
		P.append(P[0])
		P.append(P[1])
		CRUSTPIX = calcLinesSmooth(self.SMOOTHAMOUNT,P) # Creates a smooth line

		# Draw everything!
		pixels = pygame.PixelArray(surface)
		
		for (x,y,z) in COREPIX:
			if x >= 0 and x < width and y >= 0 and y < height:
				pixels[x][y] = self.colcore
			
		for (x,y,z) in CRUSTPIX:
			if x >= 0 and x < width and y >= 0 and y < height:
				pixels[x][y] = self.colcrust

		# Surface features
		for (angle, type, name, points) in self.surfacefeatures:
			a = angle+self.rotation
			
			# find the surface radius here
			pos = 0
			i = 0
			r = 1.0
			while pos < self.TWOPI:
				if angle >= pos and angle < pos+angledelta:
					r = self.crust[i%len(self.crust)]
					pos = self.TWOPI # Exit loop
				pos = pos + angledelta
				i = i+1

			P = []
			for (x,y) in points:
				featureangle = atan2(y,x)
				featureradius = sqrt(x**2+y**2)
				x = scale*r*cos(a)+featureradius*cos(featureangle+a)+ox
				y = scale*r*sin(a)+featureradius*sin(featureangle+a)+oy
				P.append((x,y,0))
			P.append(P[0])
			P.append(P[1])
			OBJPIX = calcLinesSmooth(self.SMOOTHAMOUNT,P) # Creates a smooth line
			for (x,y,z) in OBJPIX:
				if x >= 0 and x < width and y >= 0 and y < height:
					pixels[x][y] = self.colcrust				

			# The points of a surface feature are defined as if the object is based at angle 0
			