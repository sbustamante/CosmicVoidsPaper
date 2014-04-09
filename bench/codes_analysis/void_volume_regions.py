#void_volume_regions.py
#
#This code calculate an histogram of volumes for every found void region for the given lambda_th 
#value
#Usage void_volume_regions.py
#
#by: Sebastian Bustamante

execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["BOLSHOI/"]
#Number of sections
N_sec = [256]
#Smooth parameter
smooth = '_s1'
#Web Scheme
webs = ['Vweb', 'Tweb'] 

#Lambda value
Lambda_th = 0.0

#==================================================================================================
#			CONSTRUCTING REGIONS VOLUME
#==================================================================================================

N_sim = len(folds)

fig = plt.figure( figsize=(6,6) )
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()

tick_locations = np.array( [0,1,2,3,4,5,6] )
#Function to build the second axe
def tick_function(X):
    return ((10**X*(0.9765625)**3)/( 4*np.pi/3. ))**(1/3.)

for web in webs:
    i_fold = 0
    for fold in folds:
	print fold, web
		
	void_regs = np.transpose(np.loadtxt("%s/%s/%s/%d/voids%s/voids_%1.2f/void_regions.dat"%\
	(foldglobal, fold, web, N_sec[i_fold], smooth, Lambda_th )))
	    	    	
	ax1.hist( np.log10(void_regs[1]) , bins=30, linewidth = 3,\
	label = "%s"%(web), normed = True, histtype = 'step', cumulative = False   )
    

#Axe 1    
ax1.grid()
ax1.set_ylabel( "Normed distribution" )
ax1.set_xlabel( "Comoving volume $\log_{10}[ (0.98$ Mpc $h^{-1} )^{-3} ]$" )
ax1.legend(fancybox = True, shadow = True)

#Axe 2
ax2.set_xticks( tick_locations )
tick_label = []
for tick in tick_locations:
    tick_label.append( "%1.2f"%tick_function(tick) )
ax2.set_xticklabels( tick_label )
ax2.set_xlabel( "Equivalent spherical comoving radius Mpc $h^{-1}$" )

plt.show()