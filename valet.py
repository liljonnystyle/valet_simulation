from random import random

class Valet:
	def __init__(self, maxx, maxy):
		self.locx = random() * maxx
		self.locy = random() * maxy

		# ASSUME available time to be -24 hours because
		# we know 24 hours ahead of time where customers will be
		self.avail_time = -1440