Valet Simulation
================

This project simulates an idealized world with customers, valet drivers, and garages. Given the predetermined schedule of all customers (i.e., location, drop off time, and pick up time) and the location of all garages, the goal is to determine through simulation the minimum number of valet drivers needed to have on-demand valet. Valets are assumed to walk to locations at a speed of 6 km/hr and drive at a speed of 30 km/hr.

language used:
 * python

python libraries used:
 * random
 * numpy
 * matplotlib

###General Approach
In order to find the number of valet drivers, I increment the number of valet drivers for each simulation. To obtain more accurate results, each simulation is repeated a number of times for ensemble averaging.

The key to keeping things organized is to create a queue (i.e., a scheduler or instruction event log) for valet drivers to follow. The way I implemented it, the queue is a nested dictionary keyed on arrival times (the time needed to stay on schedule). The value is a dictionary which includes start location, end location, and end time. This queue is pre-computed prior to any simulation.

Valet drivers are given instructions based on their estimated time of arrival (ETA) for each item in the queue. The ETA is computed by taking the distance between each queue start location and the valet's next available location. A necessary complexity is that valets are not available until they have completed their previous instruction.

For each simulation, the cumulative customer waiting time is recorded. The first simulation which results in a zero waiting time is determined to be the minimum number of valets required.