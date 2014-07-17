#void_intertia_tensor_all.py
#
#This code computes distributions of the eigenvalues of the blackuced intertia tensor of each void 
#region found by each void scheme. The eigenvalues were sorted such as Lambda1 < Lambda2 < Lambda3.
#Here it will be calculated non-integrated and normed distributions of Lambda1/Lambda2 and 
#Lambda1/Lambda3 in order to determinate the shape of void regions.
#Usage void_intertia_tensor.py  <show(0) or save(1)>
#
#by: Sebastian Bustamante

execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
simulation = "BOLSHOI/"
#Number of sections
N_sec = 256
#Box lenght [Mpc]
L_box = 250.
#Web Scheme
web = ["Tweb", "Vweb", "Tweb"]
#Void parameters ( Nth-order median filtering,  Boolean for boundary removals )
config = ["21", "31", "51"]
#Void finder scheme
void_scheme = ["FAG", "FAG", "DLG"]
#Labels
labels = ["Tweb FA-WT", "Vweb FA-WT", "Density-WT"]
linestyles = ["-", "--", ":"]
#Nbins of each histogram
Nbins = 10
#Minim radius for a void
rmins = [0,1.7,0]

#Bins radials
rbins = [ 1.0, 3.0, 8.0, 20.0 ]
rbins = [ 1.0, 4.0, 20.0 ]
colors = [ "blue", "green", "red" ]

#==================================================================================================
#			COMPUTING EIGENVALUES AND BUILDING THE INERTIA TENSOR
#==================================================================================================

#Effective radius function
def r_eff(X):
    return ((10**X*(0.9765625)**3)/( 4*np.pi/3. ))**(1/3.)

plt.figure( figsize=(16,5) )

i = 0
for i in xrange(3):

    print simulation

    #Loading intertia eigenvalues
    eigen = np.transpose(np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%s/eigen.dat"%\
    (foldglobal, simulation, web[i], N_sec, void_scheme[i], config[i] )))
    #Loading catalog of voids
    catalog = np.transpose(np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%\
    (foldglobal, simulation, web[i], N_sec, void_scheme[i], config[i] )))
    catalog = catalog[:,catalog[1]>=catalog[1,len(eigen[0])-1]]

    reff = r_eff(np.log10(catalog[1]))
    rmin = rmins[i]
    
    for i_r in xrange(len(rbins)-1):
	plt.subplot(1,2,1)
	hist, t01 = np.histogram( eigen[0,(reff>=rbins[i_r])*(reff<rbins[i_r+1])]/eigen[1,(reff>=rbins[i_r])*(reff<rbins[i_r+1])],
	bins = Nbins, normed = True )
	plt.plot( t01[:-1], hist, color=colors[i_r], linewidth = 2, linestyle = linestyles[i] )
	
	plt.subplot(1,2,2)
	hist, t12 = np.histogram( eigen[1,(reff>=rbins[i_r])*(reff<rbins[i_r+1])]/eigen[2,(reff>=rbins[i_r])*(reff<rbins[i_r+1])],
	bins = Nbins, normed = True )
	plt.plot( t12[:-1], hist, color=colors[i_r], linewidth = 2, linestyle = linestyles[i] )


    #Number of anisotropic voids
    N_tot = len(eigen[0])*1.0
    t1t2 = eigen[0]/eigen[1]
    t2t3 = eigen[1]/eigen[2]
    #Number of anisotropic voids
    print "Number of voids: ", N_tot
    print "Anisotropic voids: ", np.sum( (t1t2<0.7)*(t2t3<0.7) )/N_tot
    print "Isotropic voids: ", np.sum( (t1t2>=0.7)*(t2t3>=0.7) )/N_tot
    print "Pancake voids: ", np.sum( (t1t2<0.7)*(t2t3>=0.7) )/N_tot
    print "Filament voids: ", np.sum( (t1t2>=0.7)*(t2t3<0.7) )/N_tot
	
plt.subplots_adjust( right = 0.98, top = 0.95, left = 0.05, wspace=0.08 )

if sys.argv[1] == '1':
    plt.savefig( '%svoids_inertia_tensor.pdf'%(figures_fold) )
else:
    plt.show()