#monte_carlo_FA.py
#
#This code makes a MonteCarlo studying of the FA function as defined in Libeskind12 in order to 
#determine values of the FA according to the geometry.
#Usage monte_carlo_FA.py
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
webs = ['Tweb', 'Vweb'] 
#Colors
colors = ['green', 'blue']
#Void finder scheme (FOF or LAY)
void_scheme = 'LAY'
#Lambda values
Lambda_th = np.arange( 0, 1.0, 0.01 )

#==================================================================================================
#			CONSTRUCTING REGIONS VOLUME
#==================================================================================================
if sys.argv[1] == '1':
    plt.savefig( '%svoids_regions_percolation_%s.pdf'%(figures_fold,void_scheme) )
else:
    plt.show()