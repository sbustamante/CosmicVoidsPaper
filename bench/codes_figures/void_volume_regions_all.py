#void_volume_regions_all.py
#
#This code calculate an volume functions for each void finder scheme
#Usage void_volume_regions_all.py <normal(0) or cumulative(1)> <show(0) or save(1)>
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
labels = ['FA-Tweb', 'FA-Vweb', 'Density']
#Void finder scheme (FAG or FOF)
void_scheme = 'FAG'
#Schemes used for each web
schemes = [ "21","31","51" ]

#Colors
colors = ["green", "blue", "red"]

#==================================================================================================
#			CONSTRUCTING REGIONS VOLUME
#==================================================================================================

fig = plt.figure( figsize=(5,5) )
fig.subplots_adjust( top = 0.9, right = 0.98, left = 0.12, wspace = 0.05, bottom = 0.1 )
ax1 = [fig.add_subplot(1,1,i+1) for i in xrange(1)]
ax2 = [ax1[i].twiny() for i in xrange(1)]

tick_locations = np.linspace(0,4,5)
#Function to build the second axe
def tick_function(X):
    return ((10**X*(0.9765625)**3)/( 4*np.pi/3. ))**(1/3.)

i_web = 0
for web in webs:
    print simulation, web

    #DENSITY WATERSHED TRANSFORM
    if web == 'DLG':
	void_regs = np.transpose(np.loadtxt("%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%\
	(foldglobal, simulation, "Tweb", N_sec, web, schemes[i_web] )))
    #FA WATERSHED TRANSFORM    
    else:
	void_regs = np.transpose(np.loadtxt("%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%\
	(foldglobal, simulation, web, N_sec, void_scheme, schemes[i_web] )))

    hist1d = np.histogram( np.log10(void_regs[1]) , bins=20, normed=False )
    
    #Normal distribution
    if sys.argv[1] == '0':
	distro = hist1d[0]
    #Cumulative distribution
    else:
	distro = np.cumsum(hist1d[0][::-1])[::-1]
	
    #Plot
    ax1[0].semilogy( hist1d[1][:-1], distro, linewidth = 2.0, linestyle = "-",\
    color = colors[i_web], label = "%s (%s-order MF)"%(labels[i_web], schemes[i_web][0]) )
      
    i_web += 1
    
#Format of plots
for i in range(1):
    #Axe 1
    ax1[i].grid()
    ax1[i].set_xticks( np.linspace(0,5,6) )
    ax1[i].set_xlim( (0,4.5) )
    
    ax1[i].set_ylabel( "Number of voids" )
    ax1[i].set_xlabel( "Comoving volume $\log_{10}[ (0.98$ Mpc $h^{-1} )^{-3} ]$" )
    ax1[i].legend( loc='upper right', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )

    #Axe 2
    ax2[i].set_xlim( (0,4.5) )
    ax2[i].set_xticks( tick_locations )
    tick_label = []
    for tick in tick_locations:
	tick_label.append( "%1.1f"%tick_function(tick) )
    ax2[i].set_xticklabels( tick_label )
    ax2[i].set_xlabel( "Effective radius Mpc $h^{-1}$" )

if sys.argv[2] == '1':
    plt.savefig( '%svoids_regions_volume_all.pdf'%(figures_fold) )
else:
    plt.show()