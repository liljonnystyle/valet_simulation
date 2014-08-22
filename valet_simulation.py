#!/usr/bin/python
from customer import Customer
from valet import Valet
from random import random
import numpy as np
import matplotlib.pylab as plt

def instantiate_world(n_C, n_G, maxx, maxy):
	customers = []

	for i in xrange(n_C):
		customers.append(Customer(maxx, maxy))
	
	garages = []
	for i in xrange(n_G):
		x = random()*maxx
		y = random()*maxy
		garages.append((x,y))

	return customers, garages

def precompute_queue(customers,garages):
	'''
	Generate instructions for valet drivers as a queue.
	INPUT:
		customers - list of customer class objects
		garages - list of garage locations (tuples)
	OUTPUT:
		queue - nested dictionary keyed on pickup times.
			Inner dictionary contains pickup location,
			dropoff location, and dropoff time. E.g.,
		queue = {
		21: {pickup: (x,y), dropoff: (x,y), drop_time: 25},
		24: {pickup: (x,y), dropoff: (x,y), drop_time: 27},
		26: {pickup: (x,y), dropoff: (x,y), drop_time: 30},
		...
		}
	'''

	queue = {}
	for c in customers:
		r2min = 100
		garage_min = -1
		for i, g in enumerate(garages):
			r2 = (g[0]-c.locx)**2 + (g[1]-c.locy)**2
			if r2 < r2min:
				r2min = r2
				garage_min = i

		eta = r2min**(0.5)/0.5 # speed is 0.5 km/min = 30 km/hr

		if c.leaving_time - c.time < 2*eta:
			# pick up car but not enough time to drop off at garage
			inner_dict = {'pickup': (c.locx,c.locy),
						'dropoff': (c.locx,c.locy),
						'drop_time': c.leaving_time}
			queue[c.time] = inner_dict
		else:
			# instructions to pick up car from customer and deliver to garage
			inner_dict = {'pickup': (c.locx,c.locy),
						'dropoff': garages[i],
						'drop_time': c.time+eta}
			queue[c.time] = inner_dict

			# instructions to pick up car from garage and deliver to customer
			inner_dict = {'pickup': garages[i],
						'dropoff': (c.locx,c.locy),
						'drop_time': c.leaving_time}
			queue[c.leaving_time-eta] = inner_dict
	return queue

def simulate(customers,garages,valets,queue):
	'''
	Run simulation.
	INPUT:
		customers - list of customer class objects
		garages - list of garage locations (tuples)
		valets - list of valet class objects
		queue - nested dictionary of valet instruction events
	OUTPUT:
		wait_time - cumulative waiting time for all customers
	'''

	wait_time = 0

	for time in sorted(queue.keys()):
		event = queue[time]

		eta_min = 2880
		valet_min = -1
		for i, v in enumerate(valets):
			r2 = (v.locx-event['pickup'][0])**2 + (v.locy-event['pickup'][1])**2
			eta = r2**(0.5)/0.1 + v.avail_time
			# eta is the earliest time this valet can arrive at pickup location
			if eta < eta_min:
				eta_min = eta
				valet_min = i

		# if soonest valet will be late, accumulate customer wait time
		late = eta_min - time
		if late > 0:
			wait_time += late
			valets[valet_min].avail_time = event['drop_time']+late
		else:
			valets[valet_min].avail_time = event['drop_time']
		valets[valet_min].locx = event['dropoff'][0]
		valets[valet_min].locy = event['dropoff'][1]

	return wait_time

def main():
	n_C = 20
	n_G = 10
	n_sims = 50

	# assume world is 10 km x 10 km
	maxx = 10
	maxy = 10

	customers, garages = instantiate_world(n_C, n_G, maxx, maxy)

	queue = precompute_queue(customers, garages)

	wait_times = []
	for n_V in xrange(2*n_C): # try up to 2*n_C valets
		for j in xrange(n_sims): # run n_sims ensemble simulations
			valets = []
			for i in xrange(n_V+1):
				valets.append(Valet(maxx, maxy))
			if j == 0:
				wait_times.append(simulate(customers,garages,valets,queue))
			else:
				wait_times[-1] += simulate(customers,garages,valets,queue)
		wait_times[-1] /= 1.0*n_sims*n_C # average wait time per customer

	# for i, wait_time in enumerate(wait_times):
	# 	print str(i+1) + ' valets yields ' + format(wait_time,'.2f') + ' minutes delay per customer'

	print str(np.nonzero(wait_times)[0][-1]+2) + ' valets'

	# plt.figure(figsize=(15,15))
	# plt.plot(range(len(wait_times)),wait_times)

if __name__ == '__main__':
	main()
