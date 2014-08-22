from random import random

class Customer:
	def __init__(self, maxx, maxy):
		self.time = random() * 1440
		self.locx = random() * maxx
		self.locy = random() * maxy
		self.leaving_time = random() * 1440

		# make sure leaving time is after arriving time
		while self.leaving_time <= self.time:
			self.leaving_time = random() * 1440

