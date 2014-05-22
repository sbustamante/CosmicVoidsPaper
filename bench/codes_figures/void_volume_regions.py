#void_volume_regions.py
#
#This code calculate an histogram of volumes for every found void region for the given lambda_th 
#value
#Usage void_volume_regions.py <lambda_th=0.0(0) or lambda_th=optimal(1)> <show(0) or save(1)>
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
webs = ['Vweb', 'Tweb'] 
#Void finder scheme (FOF or LAY)
void_scheme = 'FAG'

#Lambda value
if sys.argv[1] == '0':
    Lambda_th = [ 0.0, 0.0 ]
if sys.argv[1] == '1':
    Lambda_th = [ 0.20, 0.36 ]

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
	    
    void_regs = np.transpose(np.loadtxt("%s/%s/%s/%d/voids%s/voids_%1.2f/void_regions.dat"%\
    (foldglobal, simulation, web, N_sec, void_scheme, Lambda_th[i_web] )))

    hist1d = np.histogram( np.log10(void_regs[1]) , bins=20, normed=False )
    
    ax1.semilogy( hist1d[1][:-1], hist1d[0], linewidth = 3, label = "%s"%(web))
    i_web += 1
    

#Axe 1    
ax1.grid()
ax1.set_ylabel( "Number of voids" )
ax1.set_xlabel( "Comoving volume $\log_{10}[ (0.98$ Mpc $h^{-1} )^{-3} ]$" )
ax1.legend(fancybox = True, shadow = True, loc = 'lower left')
ax1.set_ylim( (0,1e4) )

#Axe 2
ax2.set_xticks( tick_locations )
tick_label = []
for tick in tick_locations:
    tick_label.append( "%1.2f"%tick_function(tick) )
ax2.set_xticklabels( tick_label )
ax2.set_xlabel( "Effective comoving radius Mpc $h^{-1}$" )

if sys.argv[2] == '1':
    if sys.argv[1] == '0':
	plt.savefig( '%svoids_regions_volume_%s_null.pdf'%(figures_fold,void_scheme) )
    else:
	plt.savefig( '%svoids_regions_volume_%s_opt.pdf'%(figures_fold,void_scheme) )
else:
    plt.show()