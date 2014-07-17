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
#Nbins of each histogram
Nbins = 20
Nbins2D = 10
#Minim radius for a void
rmins = [0,1.7,0]

prop1_hist = 5
prop2_hist = 5

#==================================================================================================
#			COMPUTING EIGENVALUES AND BUILDING THE INERTIA TENSOR
#==================================================================================================

#Effective radius function
def r_eff(X):
    return ((10**X*(0.9765625)**3)/( 4*np.pi/3. ))**(1/3.)

fig, axes = plt.subplots(1,3, figsize=(16,5), sharex=True, sharey=True)

i = 0
for ax in axes.flat:

    print simulation

    #Loading intertia eigenvalues
    eigen = np.transpose(np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%s/eigen.dat"%\
    (foldglobal, simulation, web[i], N_sec, void_scheme[i], config[i] )))
    #Loading catalog of voids
    catalog = np.transpose(np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%\
    (foldglobal, simulation, web[i], N_sec, void_scheme[i], config[i] )))
    catalog = catalog[:,catalog[1]>=catalog[1,len(eigen[0])-1]]
    #Histogram of voids
    Hist_lambd  = np.transpose(np.histogram2d( eigen[0]/eigen[1], eigen[1]/eigen[2], 
    bins = Nbins2D, normed = False, range = ((0,1),(0,1))  )[0][::,::-1])

    #2D histogram
    #map2d = plt.imshow( Hist_lambd[::,::], interpolation='nearest', aspect = 'auto',
    #cmap = 'binary', extent = (0,1,0,1) )	
    #Scatter
    reff = r_eff(np.log10(catalog[1]))
    rmin = rmins[i]
    scatter = ax.scatter( eigen[0,reff>rmin]/eigen[1,reff>rmin], eigen[1,reff>rmin]/eigen[2,reff>rmin], 
    c = np.log10(reff[reff>rmin]), s=50, marker='.',linewidth=0.01, cmap='jet', vmin = 0.1, vmax = 1.2, alpha=0.6 )

    #Countorn
    CS = ax.contour( Hist_lambd[::-1,::], 7, aspect = 'auto', zorder=2,
    extent = (0,1,0,1),linewidths=1, interpolation = 'gaussian', colors="black" )
    ax.clabel(CS, inline=1, fontsize=10, fmt = "%d" )

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
	
    ax.set_ylim( (0,1) )
    ax.set_xlim( (0,1) )

    ax.grid( color='black', linestyle='--', linewidth=1., alpha=0.3 )
    ax.set_xticks( np.linspace( 0,1,Nbins/2.+1 ) )
    ax.set_yticks( np.linspace( 0,1,Nbins/2.+1 ) )
    ax.set_xlabel( "$\\tau_1/\\tau_2$", fontsize=15 )
    if i == 0:
	ax.set_ylabel( "$\\tau_2/\\tau_3$", fontsize=15 )

    ax.hlines( 0.7, 0.0, 0.7, linestyle="--", color="black", linewidth=2.5 )
    ax.text( 0.35, 0.81, "Pancake\nvoids", fontweight="bold", color="black",\
    fontsize=12, horizontalalignment="center" )

    ax.vlines( 0.7, 0.0, 0.7, linestyle="--", color="black", linewidth=2.5 )
    ax.text( 0.85, 0.3, "Filamentary\nvoids", fontweight="bold", color="black",\
    fontsize=12, horizontalalignment="center" )

    ax.hlines( 0.7, 0.7, 1.0, linestyle="--", color="black", linewidth=2.5 )
    ax.vlines( 0.7, 0.7, 1.0, linestyle="--", color="black", linewidth=2.5 )
    ax.text( 0.85, 0.81, "Isotropic\nvoids", fontweight="bold", color="black",\
    fontsize=12, horizontalalignment="center" )
    ax.text( 0.35, 0.3, "Anisotropic\nvoids", fontweight="bold", color="black",\
    fontsize=12, horizontalalignment="center" )

    ax.text( 0.01, 0.01, labels[i], fontweight="bold", color="black", fontsize=12 )
    i+=1

#Colorbar
fig.subplots_adjust( right = 0.92, top = 0.95, left = 0.05, wspace=0.08 )
cbar_ax = fig.add_axes([0.92, 0.15, 0.05, 0.7], aspect=20)
cb = fig.colorbar( scatter, orientation = "vertical", cax=cbar_ax )
cb.set_label( "$r_{eff}$ [$h^{-1}$ Mpc]", labelpad=1, fontsize=12 )
#Ticks
ticks = np.linspace( 0.1,1.2,10 )
cb.set_ticks( ticks )
cb.set_ticklabels( ['{0:3.1f}'.format(10**t) for t in ticks] )
#Set the colorbar
scatter.colorbar = cb


if sys.argv[1] == '1':
    plt.savefig( '%svoids_inertia_tensor.pdf'%(figures_fold) )
else:
    plt.show()