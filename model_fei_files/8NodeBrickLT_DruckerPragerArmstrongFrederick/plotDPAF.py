import scipy as sp
import matplotlib.pylab as plt
import h5py
import subprocess

Nsteps     = 1000
files = ["druckeraf_shearing.h5.feioutput"]
labels = [ "DPAF"]
symbols = [ ".", "+"]
maxgam = 0
maxtau = 0
plt.figure(1).set_size_inches(6, 4 , forward=True)
plt.figure(2).set_size_inches(6, 4 , forward=True)
plt.figure(3).set_size_inches(6, 4 , forward=True)
plt.figure(4).set_size_inches(6, 4 , forward=True)



for filename,lab,sym in zip(files, labels, symbols):
    print "Working on: ", filename
    f = h5py.File(filename)

    t = f["/time"]


    e = f["/Model/Elements/Outputs"][0:6,:-1]
    ep = f["/Model/Elements/Outputs"][6:12,:-1]
    s = f["/Model/Elements/Outputs"][12:,:-1]

    gamxz = e[4,:]*2
    evol = e[0:3,:].sum(axis=0)
    tauxz = s[4,:]/1000 #Convert to kPas
    # p = -s[0:3,:].sum(axis=0)
    # q = sp.sqrt( 1.5*((s[0,:] + p)**2 + (s[1,:] + p)**2 + (s[2,:] + p)**2 + 2*s[3,:]**2 + 2*s[4,:]**2 + 2*s[5,:]**2 ))

    # p = p/1000
    # q = q/1000


    sx = s[0,:]/1000
    sy = s[1,:]/1000
    sz = s[2,:]/1000
    sxy = s[3,:]/1000
    sxz = s[4,:]/1000
    syz = s[5,:]/1000

    p = -(sx+sy+sz)/3
    I1  = sx + sy + sz
    I2  =  sx*sy + sy*sz + sz*sx - sxy**2 - sxz**2 - syz**2 
    I3  = sx*sy*sz - sx*(syz**2) - sy*(sxz**2) - sz*(sxy**2) + 2*sxy*sxz*syz
    num = ( 2*I1**3 - 9*I1*I2 + 27*I3)
    den = (2*(I1**2 - 3*I2)**(1.5))

    arg = num/den
    arg[ sp.logical_and(den==0,num == 0)] = 1
    arg[sp.logical_and(den==0, abs(num) > 0 )] = 0

    arg[abs(arg)>0]=0


    phi_ = sp.arccos(arg)/3

    #These are not principal stresses, but I can get away with computing q from here
    s1 = I1/3. + 2./3.*sp.sqrt(I1**2 - 3*I2)*sp.cos(phi_)
    s2 = I1/3. + 2./3.*sp.sqrt(I1**2 - 3*I2)*sp.cos(phi_ + 2./3.*sp.pi)
    s3 = I1/3. + 2./3.*sp.sqrt(I1**2 - 3*I2)*sp.cos(phi_ + 4./3.*sp.pi)


    sigma = sp.vstack((s1,s2,s3))
    sigma = sp.sort(sigma, axis=0 )

    sig1 = sigma[2,:]
    sig2 = sigma[1,:]
    sig3 = sigma[0,:]

    # q = (sig1 - sig3)/2
    q = sp.sqrt(((sig1 - sig2)**2 + (sig1 - sig3)**2 + (sig2 - sig3)**2)/2)
    p = -(sig1 + sig2 + sig3)/3



    maxgam = max((maxgam,max(abs(gamxz*100))))
    maxtau = max((maxtau,max(abs(tauxz))))

    plt.figure(1)
    plt.plot(gamxz*100, tauxz, label = lab,  linewidth=2)
    # plt.plot(gamxz[0], tauxz[0], "o")
    
    plt.figure(2)
    plt.plot(evol*100, p, label = lab,  linewidth=2)

    plt.figure(3)
    plt.plot(p, q, label = lab,  linewidth=2)




    plt.figure(4)
    g_gmax = sp.diff(tauxz)/sp.diff(gamxz)
    gamxz_av = (gamxz[0:-1] + gamxz[1:])/2

    plt.semilogx(gamxz_av[:Nsteps-1], g_gmax[:Nsteps-1]/g_gmax[0],  label =lab, linewidth=2)
# maxtau = 400
plt.figure(1)
plt.xlim([-maxgam, maxgam])
plt.ylim([-1.1*maxtau, 1.1*maxtau])
plt.grid()
plt.legend(loc="upper left", framealpha=0)
plt.xlabel("Shear Strain, $\gamma_{xz}$ [%]")
plt.ylabel("Shear Stress, $\\tau_{xz}$ [KPa]")


plt.figure(2)
plt.legend(loc="upper right", framealpha=0)
plt.grid()
plt.ylabel("Mean Stress, $p$ [KPa]")
plt.xlabel("Volumetric Strain, $\epsilon_{vol}$ [%]")

plt.figure(3)
plt.grid()
plt.legend(loc="lower left", framealpha=0)
plt.xlabel("Mean Stress, $p$ [KPa]")
plt.ylabel("Stress Deviator, $q$ [KPa]")
pmin, pmax = plt.xlim()
qmin, qmax = plt.ylim()
for phival in  [30, 25, 20, 15, 10]:
    phid = sp.pi*phival/180
    Meq = 6*sp.sin(phid) / (3 - sp.sin(phid))
    print "phi = {}, M = {}".format(phival, Meq) 
    p_ = sp.array([pmin, min(pmax, qmax/Meq)])
    y = Meq*p_
    plt.plot(p_, y ,"--",color=[0.7,0.7,0.7])
    # plt.plot(p_, y ,"--",color=[0.7,0.7,0.7])
    plt.text(p_[-1], y[-1], "${}".format(phival)+"^{\circ}$")




plt.figure(4)
plt.grid()
plt.ylim([0,1.1])
plt.legend(loc="lower left", framealpha=0)
plt.xlabel("Shear Strain, $\gamma_{xz}$")
plt.ylabel("Modulus Reduction, $G/G_{\max}$")

prefix = "case2"
suffix = "stress_controlled"


plt.figure(1)
plt.savefig(prefix+"_taugamma_"+suffix+".pdf", bbox_inches='tight')

plt.figure(2)
plt.savefig(prefix+"_evolp_"+suffix+".pdf", bbox_inches='tight')

plt.figure(3)
plt.savefig(prefix+"_pq_"+suffix+".pdf", bbox_inches='tight')

plt.figure(4)
plt.savefig(prefix+"_ggmax_"+suffix+".pdf",  bbox_inches='tight')

plt.show()

