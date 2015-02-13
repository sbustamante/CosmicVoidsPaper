#void_radial_density_bins.py
#
#This code computes radial histograms of the density profile of voids as computed by the three 
#defined schemes
#
#Usage: run void_radial_density_bins.py <Vweb or Tweb> <FAG or DLT> <undercomp(0) overcomp(1)> 
#<show(0) or save(1)> <no label(0) or label(1)>
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
#Configuration 
config = "01"
#Compensated
comp = int(sys.argv[3])

#Number of middle points for mapping the density field
N = 80
#Number of times the effective radius of the void
Rreff = 8
#Effective radial bins 
RadBins = [ 2.0, 3.2, 4.4, 5.6, 6.8, 8.3, 12 ]
#Colors 
#color = ["#000000","#000066", "#0000BE", "#067EF4", "#23F0D5", "#67BD65", "#FFFF00", "#FF8000", "#FF0000", "#800000"]
#color = ["#000066", "#0000BE", "#067EF4", "#23F0D5", "#67BD65", "#FFFF00", "#FF8000", "#FF0000", "#800000"]
color = ["#0000BE", "#067EF4", "#67BD65", "#FFFF00", "#FF8000", "#FF0000", "#800000"]
#Linewidths
linewidths = [ 2, 2.25, 2.5, 2.75, 3.0, 3.25 ]
#Labels 
labels = { "FAG":"FA-WT", "DLG":"Density-WT" }
#Compensated
comp_label = ["Subcompensated", "Overcompensated"]

#Effective radius function
def r_eff(X):
    return ((10**np.log10(X)*(0.9765625)**3)/( 4*np.pi/3. ))**(1/3.)

#==================================================================================================
#			COMPUTING RADIAL PROFILES OF DENSITY FOR EVERY RADIAL BIN
#==================================================================================================
fig = plt.figure( figsize=(5.8,5) )
ax = fig.add_subplot(111)

for ri in xrange( len(RadBins)-1 ):
    reff_range = [ RadBins[ri],RadBins[ri+1] ]
    #Loading index of voids
    voids = np.loadtxt("%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%\
    (foldglobal, simulation, web, N_sec, void_scheme, config ))
    #Loading compensated
    compensated = np.loadtxt("%s/%s/%s/%d/voids%s/voids_%s/comp_half.dat"%\
    (foldglobal, simulation, web, N_sec, void_scheme, config ))
  
    indexes = voids[ (reff_range[0]<=r_eff(voids[:,1])) & (r_eff(voids[:,1])<reff_range[1]) & ( compensated[:,1] == comp ) ,0 ]
    print len(indexes)
    #Calculating median and quartiles
    median = np.zeros( N )
    Q1 = np.zeros( N )
    Q2 = np.zeros( N )
    Rnorm = np.linspace( 0, Rreff, N )
    #Loading single voids
    i_r = 0
    for r in Rnorm:
        values = []
        for i in indexes:
	    try:
		rprofile = np.loadtxt('%svoids_density_%s/%s/void_%d_DR.dat'%
		(data_figures_fold,void_scheme,web,i-1))
	    except:
                pass
	    if len(rprofile)==2:
		continue
	    #interpolating and filtering nan data
	    rho = rprofile[:,1]
	    ur = rprofile[ np.isnan(rho)==False ,0]
	    rho = rho[ np.isnan(rho)==False ]
	    #Reffi = r_eff(voids[i,1])
	    #plt.plot( ur, rho, lw = 0.05 )
	    try:
		rho_interp = interp.interp1d( ur, rho )
		#Finding median and quartiles
		values.append( rho_interp( r ) )
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
    #ax.fill_between( Rnorm, Q1, Q2, alpha = 0.3, color = color[ri] )
    ax.plot( Rnorm, median, color = color[ri], linewidth = linewidths[ri], 
    label = "%1.2f$\leq$r$_{eff}$<%1.2f"%(reff_range[0],reff_range[1]) )
    #ax1.plot( Rnorm, median, color = color[ri], linewidth = 2 )
    
#Formating main plot
ax.set_ylabel( "Density contrast $\delta$" )
ax.set_xlabel( "Normalized radius $r/r_{eff}$" )
ax.set_ylim( (-1,0.5) )
ax.grid(1)
ax.set_title( "%s %s (%s)"%(web, labels[void_scheme], comp_label[comp]) )
if sys.argv[5] == '1':
    ax.legend( loc="lower right", fancybox=True, shadow=True, fontsize=9, ncol=2 )
fig.subplots_adjust( right = 0.95, left = 0.16, top = 0.94, bottom = 0.11 )


if sys.argv[4] == '1':
    plt.savefig( '%svoids_density_%s%s%s.pdf'%(figures_fold,web,void_scheme,comp) )
else:
    plt.show()