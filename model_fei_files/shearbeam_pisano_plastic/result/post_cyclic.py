#!/usr/bin/python
import scipy as sp
import matplotlib.pyplot as plt
import h5py
# import colorplot

import sys
import pylab as pl
# print sys.path

# exit(0)
# unload_prod = sp.loadtxt("unload.prod",dtype=sp.double)
# branches = sp.loadtxt("branches.txt",dtype=sp.int32)
# alphas = sp.loadtxt("alphas.txt",dtype=sp.double)

n1 = 101
n2 = 2000

# plotthese = unload_prod < 0
file_in=sys.argv[1]


colors = [ [1,0,0], [0,1,0], [0,0,1]]
markersizes = [5., 5., 20.]
f = h5py.File(file_in.format(0))
# f = h5py.File("vonmisesLT_test01.h5.feioutput".format(0))

t = f["time"][:]

exx = f["/Model/Elements/Outputs"][0,:]
eyy = f["/Model/Elements/Outputs"][1,:]
ezz = f["/Model/Elements/Outputs"][2,:]
exy = f["/Model/Elements/Outputs"][3,:]
exz = f["/Model/Elements/Outputs"][4,:]
eyz = f["/Model/Elements/Outputs"][5,:]
epxx = f["/Model/Elements/Outputs"][6,:]
epyy = f["/Model/Elements/Outputs"][7,:]
epzz = f["/Model/Elements/Outputs"][8,:]
epxy = f["/Model/Elements/Outputs"][9,:]
epxz = f["/Model/Elements/Outputs"][10,:]
epyz = f["/Model/Elements/Outputs"][11,:]
sxx = f["/Model/Elements/Outputs"][12,:]
syy = f["/Model/Elements/Outputs"][13,:]
szz = f["/Model/Elements/Outputs"][14,:]
sxy = f["/Model/Elements/Outputs"][15,:]
sxz = f["/Model/Elements/Outputs"][16,:]
syz = f["/Model/Elements/Outputs"][17,:]

print "t.shape = ", t.shape
print "sxx.shape = ", sxx.shape

gamma = 2*exz
tau = sxz/1e3
evol = -(exx + eyy + ezz)
p = -(sxx + syy + szz)/3

nt = len(t)
ns = len(sxx)

n = min((nt,ns))


#
#  Gamma - tau
#

# markers = plotthese[(i*(n1+n2) + n1):(i*(n1+n2) + n1+n2)]

fig=pl.figure(1)
plot=fig.add_subplot(111)

plot.plot(gamma[:-1], tau[:-1])
plot.tick_params(axis='both', which='major', labelsize=20)
plot.tick_params(axis='both', which='minor', labelsize=15)
pl.xlim([-0.003,0.003])
# if (i>0):
# 	plt.plot(gamma[markers], tau[markers],"ok")
plt.xlabel("Shear strain, $\\gamma [\\perthousand]$",fontsize=24)
plt.ylabel("Shear stress, $\\tau [kPa]$",fontsize=24)
plt.grid("on")

	# if (i>0):
	# 	plt.figure(2)
	# 	plt.plot(gamma[:-1], tau[:-1],".-k")

	# 	jj = 0
	# 	for label in [120, 200, 300]:
	# 		plotthese = branches==label
	# 		markers = plotthese[(i*(n1+n2) + n1):(i*(n1+n2) + n1+n2)]
	# 		plt.plot(gamma[markers], tau[markers],"o",label=str(label), color=colors[jj], markersize=markersizes[jj],alpha=0.5)
	# 		jj+=1
			
	# 	plt.legend()
	# 	plt.xlabel("Shear strain, $\\gamma [\\perthousand]$")
	# 	plt.ylabel("Shear stress, $\\tau [kPa]\$")
	# 	plt.grid("on")


	# plt.figure(2)
	# plt.plot(t[:n], tau[:n])
	# plt.xlabel("Time")
	# plt.ylabel("Shear stress, $\\tau [kPa]\$")
	# plt.grid("on")

	# plt.figure(3)
	# plt.plot(t[:n], gamma[:n])
	# plt.xlabel("Time")
	# plt.ylabel("Shear strain, $\\gamma [\\perthousand]$")
	# plt.grid("on")
	# #
	#  p - t
	#
	# plt.figure(2)
	# plt.plot(t, p[:-1]/1000)
	# plt.grid()

	# plt.xlabel(r"Time, $t [s]$")
	# plt.ylabel(r"Mean pressure, $p [kPa]$")


	# #
	# #  evol - t
	# #
	# plt.figure(3)
	# plt.plot(t, evol[:-1]*1000)
	# plt.grid()

	# plt.xlabel(r"Time, $t [s]$")
	# plt.ylabel(r"Volumetric strain, $\epsilon_{\mathrm{vol}} [\perthousand]$")


# for i in range(1):
# 	plt.figure(i+1)
# 	ax = plt.gca()
# 	lines = ax.get_lines()
# 	lines[1].set_c("r")
# 	lines[1].set_linestyle("-")
# 	lines[1].set_marker(".")


# print alphas.shape
# print alphas

# plt.figure(3)
# plt.subplot(2,1,1)
# plt.plot(alphas[:,0],label="alpha")
# plt.plot(alphas[:,1],label="alpha0")
# plt.plot(alphas[:,2],label="alpha0mem")
# plt.subplot(2,1,2)
# plt.plot(alphas[:,3],label="nij_dev")
# plt.legend()

plt.show()
file_in=file_in[:-13]
fileout=file_in+'.png'
fig.savefig(fileout,bbox_inches='tight')
