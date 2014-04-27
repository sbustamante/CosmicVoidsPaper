#void_matrix_builder.py
#
#This code builds the matrix associated with voids regions, where 0 isn't a void and 1 corresponds 
#to one. All of this for a specific lambda_th value (given). Furthermore, the FOF is implemented 
#in order to classify different regions of voids.
#Usage: void_matrix_builder.py <Tweb or Vweb>
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
#Void finder scheme (FOF or LAY)
void_scheme = 'LAY'
#Web Scheme
web = sys.argv[1]


#==================================================================================================
#			CONSTRUCTING REGIONS VOLUME
#==================================================================================================

print simulation

#Loading eigenvalues
eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,simulation,web,N_sec,smooth)

lambda_th_opt = np.arange( 0, 1.0, 0.01 )
lambda_th_opt = [0.2,]

for lamb in lambda_th_opt:
    #Building the matrix      
    void_matrix_builder( eigV_filename, lamb, N_sec, './void_matrix_\(%1.2f\).dat'%(lamb) )
    print 'Void matrix for %s: done!'%(simulation)
    
    #Building the index of FOF regions
    void_matrix = "./void_matrix_\(%1.2f\).dat"%( lamb )
    if void_scheme == 'FOF':
	void_regs = void_finder_FOF( void_matrix, ordered = True, out_folder='./voids_%1.2f'%(lamb),\
	extra_info = False, remove = False )

    #Building the index of FOF regions
    if void_scheme == 'LAY':
	seed_matrix = "%s/%s/%s/%d/voidsFOF/voids_0.00/void_index.dat"%(foldglobal, simulation, web, N_sec )
	void_regs = void_finder_LAY( void_matrix, seed_matrix, ordered = False, out_folder='./voids_%1.2f'%(lamb),\
	extra_info = True, remove = False )
	