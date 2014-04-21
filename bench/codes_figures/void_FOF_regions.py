#void_FOF_regions.py
#
#This code calculate the dependece of the volume of the largest region with the threshold value,
#furthermore, the number of voids.
#Usage void_FOF_regions.py <show(0) or save(1)>
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
webs = ['Tweb', 'Vweb'] 
#Colors
colors = ['green', 'blue']

#Lambda values
Lambda_th = np.arange( 0, 1.0, 0.01 )

#==================================================================================================
#			CONSTRUCTING REGIONS VOLUME
#==================================================================================================

plt.figure( figsize=(5,10) )
i_web = 0
for web in webs:
    print simulation, web
    
    N_voids = []
    Vol_1void = []
    
    for lamb in Lambda_th:
	void_regs = np.transpose(np.loadtxt("%s/%s/%s/%d/voids%s/voids_%1.2f/void_regions.dat"%\
	(foldglobal, simulation, web, N_sec, smooth, lamb )))
	
	N_voids.append( void_regs[0,-1] )
	Vol_1void.append( void_regs[1,0]/np.sum(1.0*void_regs[1]) )
	
    #Number of voids
    plt.subplot( 2,1,1 )
    plt.plot( Lambda_th, N_voids/N_voids[0], '-', linewidth = 2, label="%s"%(web), color = colors[i_web] )
    if web == 'Tweb':
	lamb_opt = 0.36
    elif web == 'Vweb':
	lamb_opt = 0.202
    plt.vlines( lamb_opt, 0, 2.5, linestyle = '--', color = colors[i_web], linewidth = 2 )
    plt.text( lamb_opt + 0.02, 2.5*.5, '$\lambda_{opt}^{%s}$'%(web[0]), fontsize = 12, color = colors[i_web] )
    plt.ylim( (0,2.5) )
    
    #Largest volume
    plt.subplot( 2,1,2 )
    plt.plot( Lambda_th, Vol_1void , '-', linewidth = 2, color = colors[i_web] )
    if web == 'Tweb':
	lamb_opt = 0.36
    elif web == 'Vweb':
	lamb_opt = 0.202
    plt.vlines( lamb_opt, 0, 1, linestyle = '--', color = colors[i_web], linewidth = 2 )
    plt.text( lamb_opt + 0.02, 1*.5, '$\lambda_{opt}^{%s}$'%(web[0]), fontsize = 12, color = colors[i_web] )
    plt.ylim( (0,1) )
  
    i_web += 1
    
plt.subplot( 2,1,1 )
plt.grid()
plt.ylabel( "Number of voids $N/N_0$" )
plt.xlabel( "$\lambda_{th}$" )
plt.legend(fancybox = True, shadow = True)

plt.subplot( 2,1,2 )
plt.grid()
plt.ylabel( "Largest void volume  $V/V_{all}$" )
plt.xlabel( "$\lambda_{th}$" )

if sys.argv[1] == '1':
    plt.savefig( '%svoids_regions_percolation_FOF.pdf'%(figures_fold) )
else:
    plt.show()