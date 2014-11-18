#void_radial_velocity_bins.py
#
#This code computes radial histograms of the velocity profile of voids as computed by the three 
#defined schemes
#
#Usage: run void_radial_velocity_bins.py <Vweb or Tweb> <FAG or DLT> <show(0) or save(1)>
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
N_cut = 2

#Number of middle points for mapping the density field
N = 40
#Number of times the effective radius of the void
Rreff = 8
#Effective radial bins 
RadBins = [ 2, 3, 4, 5, 6, 7, 8, 9, 10, 12 ]
#Colors 
#color = ["#000000","#000066", "#0000BE", "#067EF4", "#23F0D5", "#67BD65", "#FFFF00", "#FF8000", "#FF0000", "#800000"]
color = ["#000066", "#0000BE", "#067EF4", "#23F0D5", "#67BD65", "#FFFF00", "#FF8000", "#FF0000", "#800000"]
#Labels 
labels = { "FAG":"FA-WT", "DLG":"Density-WT" }


#Effective radius function
def r_eff(X):
    return ((10**np.log10(X)*(0.9765625)**3)/( 4*np.pi/3. ))**(1/3.)

#==================================================================================================
#			COMPUTING RADIAL PROFILES OF VELOCITY FOR EVERY RADIAL BIN
#==================================================================================================
plt.figure( figsize=(5.5,5) )
for ri in xrange( len(RadBins)-1 ):
    reff_range = [ RadBins[ri],RadBins[ri+1] ]
    #Loading index of voids
    voids = np.loadtxt('%svoids_density_%s/void_regions_%s.dat'%(data_figures_fold,void_scheme,web))
    indexes = voids[ (reff_range[0]<=r_eff(voids[:,1]))*(r_eff(voids[:,1])<reff_range[1]) ,0 ]
    #Calculating median and quartiles
    median = np.zeros( N )
    Q1 = np.zeros( N )
    Q2 = np.zeros( N )
    Rnorm = np.linspace( 0.01, Rreff, N )
    #Loading single voids
    i_r = 0
    for r in Rnorm:
        values = []
        for i in indexes:
	    try:
		vprofile = np.loadtxt('%svoids_density_%s/%s/void_%d_VR.dat'%
		(data_figures_fold,void_scheme,web,i))
	    except:
                pass
	    #interpolating
	    vel = vprofile[:,1]
	    ur = vprofile[ np.isnan(vel)==False ,0]
	    vel = vel[ np.isnan(vel)==False ]
	    Reffi = r_eff(voids[i,1])
	    	    
	    try:
		vel_interp = interp.interp1d( ur, vel )
		#Finding median and quartiles
		values.append( vel_interp(r) )
            except:
                pass
        values = np.sort(values)
        try:
	    median[i_r] = np.mean(values)
            #median[i_r] = values[ int(len(values)*0.5) ]
            #Q1[i_r] = values[ int(len(values)*0.25) ]
            #Q2[i_r] = values[ int(len(values)*0.75) ]
        except:
            pass
        i_r += 1
    median[median==0] = nan
    Q1[Q1==0] = nan
    Q2[Q2==0] = nan
    Rnorm = Rnorm[ np.isnan(median)==False ]
    Q1 = Q1[ np.isnan(median)==False ]
    Q2 = Q2[ np.isnan(median)==False ]
    median = median[ np.isnan(median)==False ]
    plt.fill_between( Rnorm, Q1, Q2, alpha = 0.3, color = color[ri] )
    plt.plot( [0]+list(Rnorm), [0]+list(median), color = color[ri], linewidth = 2, 
    label = "%1.2f$\leq$r$_{eff}$<%1.2f"%(reff_range[0],reff_range[1]) )
    
plt.ylabel( "radial velocity $v \cdot u_r$ [km/s]" )
plt.xlabel( "Normalized radius $r/r_{eff}$" )
plt.ylim( (-20,80) )
plt.grid(1)
plt.title( "%s %s"%(web, labels[void_scheme]) )
plt.legend( loc="upper right", fancybox=True, shadow=True, fontsize=9, ncol=2 )
plt.subplots_adjust( right = 0.95, left = 0.15, top = 0.95 )
if sys.argv[3] == '1':
    plt.savefig( '%svoids_velocity_%s%s.pdf'%(figures_fold,web,void_scheme) )
else:
    plt.show()