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
from Missile import Missile

class Planet:
	# Class variables shared by all instances go here
	SMOOTHAMOUNT = 3 # How many times to run Chaiken across the points
	TWOPI = pi*2.0
	MAXSPIN = TWOPI/16
	MAXRINGSIZE = 2 # pixels
	# End Class variables
	
	def __init__(self, name, radius, angvelocity, colcrust, colcore):
		# Instance variables unique to each instance go here
		self.alive = True
		self.name = name # Label the planet for easy reference later
		segments = 80*radius # initial number of sections around the circumference
		if segments < 7:
			segments = 7
		crustradius = radius
		self.radiusAvg = crustradius
		coreradius = crustradius / 3.0
		self.colcrust = colcrust
		self.colcore = colcore
		self.rotation = random()*pi*2.0
		self.crust = []
		self.core = []
		self.impacts = []
		for i in xrange(0,int(segments)):
			self.crust.append((crustradius+randint(0,5)*0.01)) # ToDo: Add height variation
			self.core.append((coreradius+randint(-3,3)*0.01)) # ToDo: Add height variation
		self.angvelocity = angvelocity # angular velocity
		self.surfacefeatures = []
		self.ringing = 0
		self.ringsize = 0
		self.debris = []
	
	def addSurfaceFeature(self, angle, type, name, points):
		self.surfacefeatures.append((angle,type,name,points))

	def rotate(self,angle):
		self.rotation = self.rotation + angle
		if self.rotation > pi:
			self.rotation = self.rotation-self.TWOPI
		if self.rotation < pi:
			self.rotation = self.rotation+self.TWOPI
		if self.angvelocity > self.MAXSPIN:
			self.angvelocity = self.MAXSPIN
		if self.angvelocity < -self.MAXSPIN:
			self.angvelocity = -self.MAXSPIN

	def impactsHandler(self):
		# An object impacted at a particular angle. Process it by adjusting the crust
		# Find out which part of the crust was affected
		if len(self.impacts) > 0:
			angledelta = pi*2.0/len(self.crust) # number of angular divisions
			halfangledelta = angledelta/2
			for (a,sz,v) in self.impacts:
				while a < -pi:
					a = a+self.TWOPI
				while a > pi:
					a = a-self.TWOPI

				angle = -pi
				i = 0
				R = [] # New crust
				SF = [] # New surface features
				
				while angle < pi and i < len(self.crust):
					# If the collision was with the surface:
					if a >= angle-halfangledelta and a < angle+halfangledelta: # impact!
						# is there a surface feature here to absorb the impact?
						breakCrust = True
						fiveangledelta = angledelta*1
						for (sfangle,sftype,sfname,sfpoints) in self.surfacefeatures:
							buildingangle = sfangle+pi
							while buildingangle < -pi:
								buildingangle = buildingangle+self.TWOPI
							while buildingangle > pi:
								buildingangle = buildingangle-self.TWOPI

							if a >= buildingangle-fiveangledelta and a < buildingangle+fiveangledelta: # Remove the surface feature
								# print "Surface feature "+sfname+" of type "+sftype+" destroyed!"
								if sz < 20:
									breakCrust = False
							else:
								SF.append( (sfangle,sftype,sfname,sfpoints) ) # Keep this surface feature
							self.surfacefeatures = SF # Replace the old list
						if breakCrust == True: # collapse the crust
							R.append((self.crust[i]-0.1*sz/10))
							# handle velocity vector
							# add spin quantum for each collision, adjusted by the vector tangent to the "a" normal
							mdir,spd = v
							mdir = mdir - a # Find the angular difference
							spd = sz*spd / 100
							angvdelta = spd*sin(mdir) # tangent
							self.angvelocity = self.angvelocity - angvdelta*pi/180
							self.ringing = self.ringing+abs(sz)+self.MAXRINGSIZE
							self.ringsize = self.ringsize+abs(sz)
							if self.ringsize > self.MAXRINGSIZE:
								self.ringsize = self.MAXRINGSIZE

							if sz >10:
								# Debris
								(debang,debspeed) = v
								newDir = -debang+self.rotation
								NUMFRAGS = randint(3,12)
								dang = pi*2.0/720
								for j in xrange(0,NUMFRAGS):								
									newMissile = Missile("Debris",(1.2*cos(angle+self.rotation+pi),1.2*sin(angle+self.rotation+pi)),(newDir+dang*randint(-15,15),debspeed/(randint(3,12)*0.25)))
									newMissileObj = Planet("Debris", 0.1, 0, (192,60,0,255), (255,100,0,255))
									self.debris.append((newMissile,newMissileObj,int(sz)>>1))

						else: # Keep this point
							R.append((self.crust[i]))
					else: # Keep this point
						R.append((self.crust[i]))
					i = i+1
					angle = angle+angledelta
				self.crust = R # Replace with a new changed crust
			self.impacts = [] # All processed, discard and start again
				
				
			
	def draw(self,surface,centre,scale):
		width = surface.get_width()
		height = surface.get_height()
		(ox,oy) = centre # View port co-ordinates to centre the planet on.
		#print centre
		
		# updates
		self.rotate(self.angvelocity)
		# Draw everything!
		pixels = pygame.PixelArray(surface)

		drawdetail = False
				
		P = [] # Points to interpolate with Chaikin
		count = 0
		angledelta = pi*2.0/len(self.crust)
		radiusAvg = 0
		for (r) in self.crust:
			radiusAvg = radiusAvg + scale*r
			a = count*angledelta+self.rotation
			d = scale*r
			x = d*cos(a)
			y = d*sin(a)

			deltax = 0
			deltay = 0
			if self.ringing > 0: # Collisions shake the planet
				gg = self.ringing/self.ringsize # tends to zero
				magnitude = self.ringsize*sin(pi/2*gg)# So it settles down
				deltax = randint(int(-self.ringsize),int(self.ringsize))*magnitude
				deltay = randint(int(-self.ringsize),int(self.ringsize))*magnitude
			P.append((x+ox+deltax,y+oy+deltay,0)) # ToDo: Utilise z. Currently ignored
			if d > 50:
				drawdetail = True
			count = count+1
		self.radiusAvg = float(radiusAvg/count)
		# print self.radiusAvg
		P.append(P[0])
		P.append(P[1])
		CRUSTPIX = calcLinesSmooth(self.SMOOTHAMOUNT,P) # Creates a smooth line
		for (x,y,z) in CRUSTPIX:
			if x >= 0 and x < width and y >= 0 and y < height:
				pixels[x][y] = self.colcrust
		
		if drawdetail == True:
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
			for (x,y,z) in COREPIX:
				if x >= 0 and x < width and y >= 0 and y < height:
					pixels[x][y] = self.colcore

			# Surface features
			for (angle, type, name, points) in self.surfacefeatures:
				
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
				a = angle+self.rotation

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
		if self.ringing > 0:
			self.ringing = self.ringing-1

			