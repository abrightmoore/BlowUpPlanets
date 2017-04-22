# @abrightmoore

class SurfaceFeature:

	# Class variables shared by all instances go here
	TWOPI = pi*2.0
	# End Class variables
	
	def __init__(self, type, name, latitude):
		this.type = type
		this.name = name
		this.latitude = latitude
	
	def draw(self, surface, basecentre, angle):
		# Render this thing at the appropriate angle from the surface of the object
		
		