#!/usr/bin/python
import h5py
import matplotlib.pylab as plt
import sys

# Go over each feioutput and plot each one.  
files=sys.argv[1:]
for thefile in files:
	finput = h5py.File(thefile)

	# Read the time and displacement
	times = finput["time"][:]
	disp = finput["/Model/Nodes/Generalized_Displacements"][8,:-1]

	# Configure the figure filename, according to the input filename.
	outfig=thefile.replace("_","-")
	outfigname=outfig.replace("h5.feioutput","pdf")

	# Plot the figure. Add labels and titles.
	plt.figure()
	plt.plot(times,disp)
	plt.grid()
	plt.xlabel("Time (second) ")
	plt.ylabel("Displacements (meter)  ")
	plt.savefig(outfigname,  bbox_inches='tight')
	# plt.show()
