#void_percolation_analysis.py
#
#This code calculate an percolation analysis of the three void finder schemes with respecto to the
#nth-order median filtering
#Usage void_percolation_analysis.py <show(0) or save(1)>
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
schemes = [ ["00","01","10","11","21","150"], ["00","01","10","11","21","101"], ["00","01","10","11","21","51",] ]

#Linestyles
linestyles = [":",":","--","--","-","-"]
#Colors
colors = ["gray", "black"]

#==================================================================================================
#			CONSTRUCTING REGIONS VOLUME
#==================================================================================================

fig = plt.figure( figsize=(4.5*len(webs),4.5) )
fig.subplots_adjust( top = 0.9, right = 0.98, left = 0.05, wspace = 0.05, bottom = 0.1 )
ax1 = [fig.add_subplot(1,len(webs),i+1) for i in xrange(len(webs))]
ax2 = [ax1[i].twiny() for i in xrange(len(webs))]

tick_locations = np.linspace(0,4,5)
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
	ax1[i_web].semilogy( hist1d[1][:-1], distro, linewidth = 2.0, linestyle = linestyles[i_iter],\
	color = colors[i_iter%2], label = "%s (%s)"%(web, iter) )
      
	i_iter += 1
	
    i_web += 1
    
#Format of plots
for i in range(len(webs)):
    #Axe 1
    ax1[i].grid()
    ax1[i].text( 0.1, 10**3.8, labels[i], fontsize = 12, fontweight = "bold" )
    ax1[i].set_xticks( np.linspace(0,5,6) )
    ax1[i].set_xlim( (0,4.5) )
    
    if i == 0:
	ax1[i].set_ylabel( "Number of voids" )
    else:
	ax1[i].set_yticks( 10**np.linspace(0,4,5) )
	ax1[i].set_yticklabels( ["" for lb in xrange(5)] )
    if i == 1:
	ax1[i].set_xlabel( "Comoving volume $\log_{10}[ (0.98$ Mpc $h^{-1} )^{-3} ]$" )
	#ax1[i].legend( fancybox = True, shadow = True, loc = 'lower left', ncol = len(webs), fontsize = 9 )

    #Axe 2
    ax2[i].set_xlim( (0,4.5) )
    ax2[i].set_xticks( tick_locations )
    tick_label = []
    for tick in tick_locations:
	tick_label.append( "%1.1f"%tick_function(tick) )
    ax2[i].set_xticklabels( tick_label )
    if i == 1:
	ax2[i].set_xlabel( "Effective comoving radius Mpc $h^{-1}$" )

if sys.argv[2] == '1':
    plt.savefig( '%svoids_regions_volume.pdf'%(figures_fold) )
else:
    plt.show()