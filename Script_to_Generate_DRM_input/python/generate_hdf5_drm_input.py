#!/bin/usr/python
# Created by Jose 
# This file reads old-format DRM input files and translates them into new HDF5-based format.
#

# This file produces a rigid body input to the DRM layer. That is, all DRM nodes have same X-direction
# displacement and acceleration. In this case a sine wave is used. This is not realistic, its
# just for demonstration purposes. DRM won't work in this case but can be used to verify input if 
# a pseudo-static analysis is done (zero density on all elements and apply loads with transient
# analysis.)

import scipy as sp
import h5py
import time

#Write elements and nodes data
elements = sp.loadtxt("DRMelements.txt",dtype=sp.int32)
exterior_nodes = sp.loadtxt("DRMexterior.txt",dtype=sp.int32)
boundary_nodes = sp.loadtxt("DRMbound.txt",dtype=sp.int32)

Ne = sp.array(exterior_nodes.size)
Nb = sp.array(boundary_nodes.size)

Nt = Ne+Nb

all_nodes = sp.hstack((boundary_nodes, exterior_nodes))
is_boundary_node = sp.zeros(Nt, dtype=sp.int32)
is_boundary_node[0:Nb] = 1

h5file = h5py.File("input.hdf5","w")

h5file.create_dataset("Elements", data=elements)
h5file.create_dataset("DRM Nodes", data=all_nodes)
h5file.create_dataset("Is Boundary Node", data=is_boundary_node)  #This array has 1 if the node at the corresponding position in "DRM nodes" array is a boundary node and zero if not

h5file.create_dataset("Number of Exterior Nodes", data=Ne)
h5file.create_dataset("Number of Boundary Nodes", data=Nb)

#Write timestamp (time format used is that of c "asctime" Www Mmm dd hh:mm:ss yyyy  example: Tue Jan 13 10:17:09 2009)
localtime = time.asctime( time.localtime(time.time()) )
h5file.create_dataset("Created",data=str(localtime))

#Generate motions

t = sp.linspace(0,10,1001)
w = 2*sp.pi/0.5
d = sp.sin(w*t)
a = -w**2*sp.sin(w*t)

#Output accelerations, displacements and time-vector

#Format is:
#
#   Accelerations has shape [3*(N_boundary_nodes + N_exterior_nodes)  ,  Ntimesteps]
#
#
#   component A[3*n], A[3*n+1], A[3*n+2] correspond to acceleration in X, Y, and Z directions at node
#   n. The tag corresponding to node n that of the n-th component of array "DRM Nodes"

#Time vector

h5file.create_dataset("Time", data=t)

acc = h5file.create_dataset("Accelerations", (3*Nt,len(t)), dtype=sp.double,chunks=(3,50))
dis = h5file.create_dataset("Displacements", (3*Nt,len(t)), dtype=sp.double,chunks=(3,50))

for node_index in range(Nt):  
	acc[3*node_index,:]   = a
	acc[3*node_index+1,:] = 0*a  #Zero acceleration in y and z
	acc[3*node_index+2,:] = 0*a
	dis[3*node_index,:]   = d
	dis[3*node_index+1,:] = 0*d  #Zero displacement in y and z
	dis[3*node_index+2,:] = 0*d



h5file.close()



