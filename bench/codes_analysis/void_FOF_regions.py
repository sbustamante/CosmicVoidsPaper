#void_FOF_regions.py
#
#This code calculate the dependece of the volume of the largest region with the threshold value,
#furthermore, the number of voids.
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
webs = ['Vweb', 'Tweb'] 

#Lambda values
Lambda_th = np.arange( 0, 1.0, 0.01 )

#==================================================================================================
#			CONSTRUCTING REGIONS VOLUME
#==================================================================================================

plt.figure( figsize=(5,2*4) )
for web in webs:
    print simulation, web
    
    N_voids = []
    Vol_1void = []
    
    for lamb in Lambda_th:
	void_regs = np.transpose(np.loadtxt("%s/%s/%s/%d/voids%s/voids_%1.2f/void_regions.dat"%\
	(foldglobal, simulation, web, N_sec, smooth, lamb )))
	
	N_voids.append( void_regs[0,-1] )
	Vol_1void.append( void_regs[1,0]/np.sum(1.0*void_regs[1]) )
	
    plt.subplot( 2,1,1 )
    plt.plot( Lambda_th, N_voids/N_voids[0], '-', linewidth = 2, label="%s"%(web) )
    
    plt.subplot( 2,1,2 )
    plt.plot( Lambda_th, Vol_1void , '-', linewidth = 2 )
  
    
plt.subplot( 2,1,1 )
plt.grid()
plt.ylabel( "Number of voids $N/N_0$" )
plt.xlabel( "$\lambda_{th}$" )
plt.legend(fancybox = True, shadow = True)

plt.subplot( 2,1,2 )
plt.grid()
plt.ylabel( "Largest void volume  $V/V_{all}$" )
plt.xlabel( "$\lambda_{th}$" )

plt.show()