import copy

from classes.location import Location

class Finger:
	def __init__(self, location, is_return):
		self.location = Location(x=location['x'], y=location['y'])
		self.actual_location = copy.deepcopy(self.location)
		self.is_return = is_return

	def reset_location(self):
		self.actual_location = copy.deepcopy(self.location)
