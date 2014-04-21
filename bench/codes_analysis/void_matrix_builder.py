#void_matrix_builder.py
#
#This code builds the matrix associated with voids regions, where 0 isn't a void and 1 corresponds 
#to one. All of this for a specific lambda_th value (given). Furthermore, the FOF is implemented 
#in order to classify different regions of voids.
#
#by: Sebastian Bustamante

execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
#folds = ["BOLSHOI/","CLUES/10909/","CLUES/16953/","CLUES/2710/"]
folds = ["BOLSHOI/"]
#Number of sections
#N_sec = [256,64,64,64]
N_sec = [256]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme
catalog = 'FOF'
#Web Scheme
web = 'Tweb'


#==================================================================================================
#			CONSTRUCTING REGIONS VOLUME
#==================================================================================================

i_fold = 0
N_sim = len(folds)

for fold in folds:
    print fold

    #Loading eigenvalues
    eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
    
    lambda_th_opt = np.arange( 0, 1.0, 0.01 )
    lambda_th_opt = [0.0]

    for lamb in lambda_th_opt:
	#Building the matrix      
	void_matrix_builder( eigV_filename, lamb, N_sec[i_fold], './void_matrix_\(%1.2f\).dat'%(lamb) )
	print 'Void matrix for %s: done!'%(fold)
	
	#Building the index of FOF regions
	void_matrix = "./void_matrix_\(%1.2f\).dat"%( lamb )
	void_regs = void_finder( void_matrix, ordered = True, out_folder='./voids_%1.2f'%(lamb),\
	extra_info = True, remove = False )
	