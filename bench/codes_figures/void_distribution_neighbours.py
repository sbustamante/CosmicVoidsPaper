#void_distribution_neighbours.py
#
#This code computes size functions of neighbours of voids according to radial size
#
#Usage: run void_distribution_neighbours.py <Vweb or Tweb> <FAG or DLT> <show(0) or save(1)>
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
#Smooth parameter
smooth = '_s1'
#Web Scheme
web = sys.argv[1]
#Void finder scheme (FAG or DLG)
void_scheme = sys.argv[2]
#Cutt of respect to the number of cells
N_cut = 1
#Configuration 
config = "01"


#Effective radial bins 
RadBins = [ 0.0, 2.0, 3.2, 4.4, 5.6, 6.8, 8.3, 12 ]
#Colors 
color = ["#000066", "#0000BE", "#067EF4", "#67BD65", "#FFFF00", "#FF8000", "#FF0000", "#800000"]
#Linewidths
linewidths = [ 1.0, 2, 2.25, 2.5, 2.75, 3.0, 3.25 ]
#Labels 
labels = { "FAG":"FA-WT", "DLG":"Density-WT" }

#Effective radius function
def r_eff(X):
    return ((10**np.log10(X)*(0.9765625)**3)/( 4*np.pi/3. ))**(1/3.)

#==================================================================================================
#			COMPUTING RADIAL PROFILES OF DENSITY FOR EVERY RADIAL BIN
#==================================================================================================
plt.figure( figsize=(2*5.8,5) )

#Lonely voids
alone_voids = []

#Sweeping radial bins
for ri in xrange( len(RadBins)-1 ):
    reff_range = [ RadBins[ri],RadBins[ri+1] ]
    #Loading index of voids
    voids = np.loadtxt("%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%\
    (foldglobal, simulation, web, N_sec, void_scheme, config ))
    #Loading compensated
    compensated = np.loadtxt("%s/%s/%s/%d/voids%s/voids_%s/comp_half.dat"%\
    (foldglobal, simulation, web, N_sec, void_scheme, config ))
  
    #Indexes of voids within the current radial bin
    indexes = voids[ (reff_range[0]<=r_eff(voids[:,1])) & (r_eff(voids[:,1])<reff_range[1]), 0 ]
    print len(indexes)
    
    #Array of sizes
    neighbour_sizes = []
    #Loading neighbours single voids
    for i in indexes:
	neighbours = np.loadtxt("%s/%s/%s/%d/voids%s/voids_%s/void_%d.ngb"%\
	(foldglobal, simulation, web, N_sec, void_scheme, config, i ))
	try:
	    Nneigh = neighbours[0]
	except:
	    Nneigh = 0	
	if Nneigh==0:
	    alone_voids.append( voids[i-1,1] )
	else:
	    for neigh in neighbours[1:]:
		try:
		    neighbour_sizes.append( voids[neigh-2,1] )
		except:
		    None
		
    #Plotting and making histogram of neighbour voids
    plt.subplot(1,2,1)
    hist1d = np.histogram( np.log10(neighbour_sizes) , bins=20, normed=False )
    plt.semilogy( r_eff(10**(hist1d[1][:-1])), hist1d[0], color = color[ri], linewidth = linewidths[ri], 
    label = "%1.2f$\leq$r$_{eff}$<%1.2f"%(reff_range[0],reff_range[1]) )
	



#Formating main plot
plt.subplot(1,2,1)
plt.ylabel( "Number of voids" )
plt.xlabel( "Effective comoving radius Mpc $h^{-1}$" )
plt.grid(1)
plt.title( "Distribution of neighbour voids %s"%(web) )
plt.legend( loc="lower center", fancybox=True, shadow=True, fontsize=9, ncol=2 )

plt.subplot(1,2,2)
hist1d = np.histogram( np.log10(alone_voids) , bins=20, normed=False )
plt.semilogy( r_eff(10**(hist1d[1][:-1])), hist1d[0], color = "black", linewidth = 2 )
plt.ylabel( "Number of voids" )
plt.xlabel( "Effective comoving radius Mpc $h^{-1}$" )
plt.grid(1)
plt.title( "Distribution of isolated voids %s"%(web) )

if sys.argv[3] == '1':
    plt.savefig( '%svoids_neighbours_%s%s.pdf'%(figures_fold,web,void_scheme) )
else:
    plt.show()