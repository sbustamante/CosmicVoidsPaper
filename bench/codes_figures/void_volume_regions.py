#void_volume_regions.py
#
#This code calculate an histogram of volumes for every found void region for the some numbers of 
#iteration for median filtering proccess
#Usage void_volume_regions.py <normal(0) or cumulative(1)> <show(0) or save(1)>
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
#Web Scheme
webs = ['Tweb', 'Vweb', 'DLG'] 
webs = ['Tweb', 'Vweb'] 
#Void finder scheme (FAG or FOF)
void_scheme = 'FAG'
#Schemes used for each web
schemes = [ ["01","11","21"], ["01","11","21"], ["00","10","20"] ]

#Linestyles
linestyles = ["-","--","-."]
#Colors
colors = ["blue", "red", "black"]

#==================================================================================================
#			CONSTRUCTING REGIONS VOLUME
#==================================================================================================

fig = plt.figure( figsize=(5,5) )
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()

tick_locations = np.array( [0,1,2,3,4,5,6] )
#Function to build the second axe
def tick_function(X):
    return ((10**X*(0.9765625)**3)/( 4*np.pi/3. ))**(1/3.)

i_web = 0
for web in webs:
    print simulation, web
    
    i_iter = 0
    for iter in schemes[i_web]:
	#DENSITY WATERSHED TRANSFORM
	if web == 'DLG':
	    void_regs = np.transpose(np.loadtxt("%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%\
	    (foldglobal, simulation, "Tweb", N_sec, web, iter )))
	#FA WATERSHED TRANSFORM    
	else:
	    void_regs = np.transpose(np.loadtxt("%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%\
	    (foldglobal, simulation, web, N_sec, void_scheme, iter )))

	hist1d = np.histogram( np.log10(void_regs[1]) , bins=20, normed=False )
	
	#Normal distribution
	if sys.argv[1] == '0':
	    distro = hist1d[0]
	#Cumulative distribution
	else:
	    distro = np.cumsum(hist1d[0][::-1])[::-1]
	    
	#Plot
	ax1.semilogy( hist1d[1][:-1], distro, linewidth = 1.5, linestyle = linestyles[i_iter],\
	color = colors[i_web], label = "%s (%s)"%(web, iter))
      
	i_iter += 1
	
    i_web += 1
    

#Axe 1    
ax1.grid()
ax1.set_ylabel( "Number of voids" )
ax1.set_xlabel( "Comoving volume $\log_{10}[ (0.98$ Mpc $h^{-1} )^{-3} ]$" )
ax1.legend( fancybox = True, shadow = True, loc = 'lower left', ncol = len(webs), fontsize = 9 )
#ax1.set_ylim( (0,1e4) )

#Axe 2
ax2.set_xticks( tick_locations )
tick_label = []
for tick in tick_locations:
    tick_label.append( "%1.2f"%tick_function(tick) )
ax2.set_xticklabels( tick_label )
ax2.set_xlabel( "Effective comoving radius Mpc $h^{-1}$" )

if sys.argv[2] == '1':
    plt.savefig( '%svoids_regions_volume.pdf'%(figures_fold) )
else:
    plt.show()