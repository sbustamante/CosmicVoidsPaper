#density_classification.py
#
#This code builds an integrated histogram of all cells in the simulation regarding their density 
#value
#Usage: density_classification.py
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
#N delta
N_delta = 300

#==================================================================================================
#			CONSTRUCTING MEDIANS OF DENSITY REGARDING LAMBDA_1
#==================================================================================================

print simulation

#Loading density
delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,simulation,N_sec,smooth)

os.system( "./Density_Classification.out %s %d"%( delta_filename, N_delta ) )
datos = np.loadtxt( "temp.tmp" )

plt.loglog( datos[:,0]+1, datos[:,1]/(N_sec**3), "-" )
plt.grid()
plt.show()