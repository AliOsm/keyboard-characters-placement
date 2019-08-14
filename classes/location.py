import math

class Location:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def euclidean_distance(self, other):
		return math.sqrt(((self.x - other.x) * (self.x - other.x)) + ((self.y - other.y) * (self.y - other.y)))
