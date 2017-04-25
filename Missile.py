# @abrightmoore
#
# A missile will erode the planet when it collides with it. For testing

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

class Missile:
	def __init__(self, name, position, velocity):
		self.alive = True
		self.name = name
		self.position = position
		self.velocity = velocity # Direction, speed
		self.age = 0
		#print position
	
	def accelerate(self,direction, speed):
		ax = speed*cos(direction)
		ay = speed*sin(direction)
		
		(dv,sv) = self.velocity
		vx = sv*cos(dv)
		vy = sv*sin(dv)
		
		nvx = vx+ax
		nvy = vy+ay
		nd = atan2(nvy,nvx)
		ns = sqrt(nvx**2+nvy**2)
		self.velocity = (nd,ns)

	def move(self):
		(x,y) = self.position
		(dv,sv) = self.velocity
		vx = sv*cos(dv)
		vy = sv*sin(dv)		
		self.position = (x+vx,y+vy)
		
	def handleCollisionWithPlanet(self,planet):
		print "handleCollisionWithPlanet" # stub
		
	def draw(self,surface,colour):
		self.age = self.age+1
		if self.age > 10000:
			self.alive = False
			
		if self.alive == True:
			# print self.position
			width = surface.get_width()
			height = surface.get_height()
			# Draw everything!
			pixels = pygame.PixelArray(surface)
			(x,y) = self.position
			if x >= 0 and x < width and y >= 0 and y < height:
				pixels[int(x),int(y)] = colour
		