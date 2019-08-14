from classes.finger import Finger

class Hand:
	def __init__(self, fingers):
		self.fingers = list()
		for finger in fingers:
			self.fingers.append(Finger(
				location=finger['location'],
				is_return=finger['is_return']
			))
