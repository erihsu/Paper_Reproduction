# -*- coding: utf-8 -*-
# @Author: mac
# @Date:   2019-10-22 20:19:53
# @Last Modified by:   mac
# @Last Modified time: 2019-10-23 20:57:31
import math
from scipy import interpolate
import copy
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import sys


class leaf:
	def __init__(self,location):
		self.location = location
		self.queue = []
	def add_to_queue(self,leaf):
		self.queue.append(leaf)



class sink:
	def __init__(self,location,group=0):
		self.location = location
		self.group = group
	def set_group(self,group):
		self.group = group


class htree:
	def __init__(self,sink_num,root_location,height,width):
		self.level = math.log(sink_num,4)
		self.root_location = root_location
		self.height = height
		self.width = width
		self.leaf_points = [leaf(location=root_location)] # list of list
		self.last_leaves = []
		self.leaf2sink_groups = []

	def generate_last_leaves(self):
		level = self.level
		if level == 1:
			cof = [-1/4,1/4]
			for i in range(2):
				for j in range(2):
					x = self.root_location[0] + cof[j]*self.width
					y = self.root_location[1] + cof[i]*self.height
					self.last_leaves.append(leaf(location=[x,y]))

		elif level == 2:
			cof = [-3/8,-1/8,1/8,3/8]
			for i in range(4):
				for j in range(4):
					x = self.root_location[0] + cof[j]*self.width
					y = self.root_location[1] + cof[i]*self.height
					self.last_leaves.append(leaf(location=[x,y]))
		elif level == 3:
			cof = [-7/16,-5/16,-3/16,-1/16,1/16,3/16,5/16,7/16]
			for i in range(8):
				for j in range(8):
					x = self.root_location[0] + cof[j]*self.width
					y = self.root_location[1] + cof[i]*self.height
					self.last_leaves.append(leaf(location=[x,y]))
		elif level == 4:
			cof = [-15/32,-13/32,-11/32,-9/32,-7/32,-5/32,-3/32,-1/32,1/32,3/32,5/32,7/32,9/32,11/32,13/32,15/32]
			for i in range(16):
				for j in range(16):
					x = self.root_location[0] + cof[j]*self.width
					y = self.root_location[1] + cof[i]*self.height
					self.last_leaves.append(leaf(location=[x,y]))
		else:
			print("level larger than 5 not supported")
	# 	cof1 = [-1/4,1/4]
	# 	cof2 = [-3/8,-1/8,1/8,3/8]
	# 	cof3 = [-7/16,-5/16,-3/16,-1/16,1/16,3/16,5/16,7/16]
	# 	cof4 = [-15/32,-13/32,-11/32,-9/32,-7/32,-5/32,-3/32,-1/32,1/32,3/32,5/32,7/32,9/32,11/32,13/32,15/32]
	def generate_leafpoints(self,center,level=0):
		if level != self.level:
			leaf1 = leaf(location=[center.location[0]-self.width/(4*2**level),center.location[1]-self.height/(4*2**level)])
			leaf2 = leaf(location=[center.location[0]+self.width/(4*2**level),center.location[1]-self.height/(4*2**level)])
			leaf3 = leaf(location=[center.location[0]-self.width/(4*2**level),center.location[1]+self.height/(4*2**level)])
			leaf4 = leaf(location=[center.location[0]+self.width/(4*2**level),center.location[1]+self.height/(4*2**level)])
			center.add_to_queue(leaf1)
			center.add_to_queue(leaf2)
			center.add_to_queue(leaf3)
			center.add_to_queue(leaf4)
			level = level + 1
			self.generate_leafpoints(leaf1,level)
			self.generate_leafpoints(leaf2,level)
			self.generate_leafpoints(leaf3,level)
			self.generate_leafpoints(leaf4,level)




	def distance(self,location1,location2):
		return math.sqrt((location1[0]-location2[0])**2+(location1[1]-location2[1])**2)


#TODO sink group is a list contain dictionary elements
	def generate_leaf_sinks_pair(self,sink_groups):
		for leaf_point in self.last_leaves:
			dis= np.inf
			for group in sink_groups:
				# group["centroid"] is a location list like [x,y]
				# group["sinks"] is a sink group contains sink0,sink1,....
				dis_new = self.distance(leaf_point.location, group["centroid"])
				if dis_new < dis:
					dis = dis_new
					current_sink_group = group["sinks"]
			self.leaf2sink_groups.append([leaf_point,current_sink_group])
			# sink_groups.remove(current_sink_group)



	def generate_topology(self,sinks):
		self.generate_last_leaves()
		self.generate_leafpoints(center=self.leaf_points[0])
		self.generate_leaf_sinks_pair(sinks)

def readSinkLocations(file_path="s1r1.txt"):
    f = open(file_path, "r")
    bounds = f.readline().split(" ")
    sinks = []

    minX = int(bounds[0])
    minY = int(bounds[1])
    maxX = int(bounds[2])
    maxY = int(bounds[3])

    # skip second Line
    f.readline()

    num_sinks_in_file = int(f.readline().split(" ")[2])

    for u in range(num_sinks_in_file):
        data = f.readline().split(" ")
        location = [int(data[1]), int(data[2])]
        sinks.append(sink(location=location))
        # update horizontal plot constraints
        if location[0] < minX:
            minX = location[0]
        elif location[0] > maxX:
            maxX = location[0]

        # update vertical plot constraints
        if location[1] < minY:
            minY = location[1]
        elif location[1] > maxY:
            maxY = location[1]
    f.close()
    shape = [minX,minY,maxX,maxY]
    return sinks, shape

def partition_sinks(sinks,cluster_num):
	X = np.array([sink.location for sink in sinks])
	kmeans = KMeans(n_clusters=cluster_num,random_state=0).fit(X)
	centroid = kmeans.cluster_centers_
	for i in range(len(sinks)):
		sinks[i].group = kmeans.labels_[i] 
	return centroid.tolist()

def group_sinks(sinks,centroids):
	sink_groups = []
	for i in range(len(centroids)):
		a_group = []
		for sink in sinks:
			if sink.group == i:
				a_group.append(sink)
		sink_groups.append({"centroid":centroids[i],"sinks":a_group})

	return sink_groups

def draw(leaf,level=0):
	max_level = 3
	if level != max_level:
		plt.plot([leaf.location[0],leaf.queue[0].location[0],leaf.queue[0].location[0]], [leaf.location[1],leaf.location[1],leaf.queue[0].location[1]],linewidth=1,c='k')
		plt.plot([leaf.location[0],leaf.queue[1].location[0],leaf.queue[1].location[0]], [leaf.location[1],leaf.location[1],leaf.queue[1].location[1]],linewidth=1,c='k')
		plt.plot([leaf.location[0],leaf.queue[2].location[0],leaf.queue[2].location[0]], [leaf.location[1],leaf.location[1],leaf.queue[2].location[1]],linewidth=1,c='k')
		plt.plot([leaf.location[0],leaf.queue[3].location[0],leaf.queue[3].location[0]], [leaf.location[1],leaf.location[1],leaf.queue[3].location[1]],linewidth=1,c='k')
		level = level + 1
		draw(leaf.queue[0],level)
		draw(leaf.queue[1],level)
		draw(leaf.queue[2],level)
		draw(leaf.queue[3],level)
def draw_connection(clock_tree):


	# draw connections between sinks and leafs
	for pairs in clock_tree.leaf2sink_groups:
		for i in range(len(pairs[1])):
			plt.plot([pairs[0].location[0],pairs[1][i].location[0]], [pairs[0].location[1],pairs[1][i].location[1]])

	# draw connections between all level leafs
	leaf_points = clock_tree.leaf_points
	draw(leaf_points[0])



def main():
	sinks,shape = readSinkLocations()
	htree_root = [int((shape[0]+shape[2])/2),int((shape[1]+shape[3])/2)]
	htree_width = shape[2] - shape[0]
	htree_height = shape[3] - shape[1]
	centroids = partition_sinks(sinks,64)
	sink_groups = group_sinks(sinks,centroids)
	print("intialize htree")
	htree_u = htree(64, htree_root, htree_height, htree_width)
	print("start generating topology")
	htree_u.generate_topology(sink_groups)

	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	print("start drawing")
	draw_connection(htree_u)

	plt.show()

if __name__ == '__main__':
	main()