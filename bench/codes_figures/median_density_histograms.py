#median_density_histogram.py
#
#This code plots histograms of median density for all type regions according to Lambda_thr values
#Usage: median_density_histogram.py <Vweb or Tweb>
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
#Smooth parameter
smooth = '_s1'
#Web Scheme
web = sys.argv[1]
#Colors and labels
colors = [ 'green', 'blue', 'red', 'gray' ]
labels = [ 'voids', 'sheets', 'filaments', 'knots' ]

#==================================================================================================
#Median contrast density
#==================================================================================================
#Loading file of quartiles
names_quartiles = []
names_quartiles.append('%svoids_delta_hist/%s/quartiles.dat'%(data_figures_fold,web) )
names_quartiles.append( '%ssheets_delta_hist/%s/quartiles.dat'%(data_figures_fold,web) )
names_quartiles.append( '%sfilaments_delta_hist/%s/quartiles.dat'%(data_figures_fold,web) )
names_quartiles.append( '%sknots_delta_hist/%s/quartiles.dat'%(data_figures_fold,web) )


plt.figure( figsize=(5,5) )
#Median contrast density for each region
for i in xrange(4):
    #plt.subplot( 1,4,i+1 )
    quartiles = np.loadtxt( names_quartiles[i] )
    quartiles[:,[1,2,3]] = np.log( quartiles[:,[1,2,3]] + 1.0 )
    plt.fill_between( quartiles[:,0], quartiles[:,1], quartiles[:,3], color = colors[i], alpha = 0.3 )
    plt.plot( quartiles[:,0], quartiles[:,1], color = colors[i], linewidth = 1 )
    plt.plot( quartiles[:,0], quartiles[:,2], color = colors[i], linewidth = 2, label = labels[i] )
    plt.plot( quartiles[:,0], quartiles[:,3], color = colors[i], linewidth = 1 )
    
#Plot format
plt.hlines( 0, 1, 0, linestyle='--', linewidth = 2 )
plt.grid(1)
plt.ylabel( '$log(\\bar{\delta}+1)$', fontsize = 12 )
plt.xlabel( '$\lambda_{th}$', fontsize = 12 )
plt.xlim( (0,1) )
plt.legend( loc='lower right', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )
plt.title( web )
plt.savefig( '%smedian_environments_densities_%s.pdf'%(figures_fold, web) )