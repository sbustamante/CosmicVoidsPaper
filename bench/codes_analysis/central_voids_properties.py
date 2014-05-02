#central_voids_properties.py
#
#This code builds a data structure with local minimums regarding the FA index over all cells of the
#simulation for each web scheme
#Usage: central_voids_properties.py <Tweb or Vweb> <Number of cells per neighbourhood>
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
web = sys.argv[1]
#Number of neighbour cells
b = int(sys.argv[2])

#==================================================================================================
#			CONSTRUCTING MEDIANS OF DENSITY REGARDING LAMBDA_1
#==================================================================================================

print simulation

#Loading eigenvalues
eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,simulation,web,N_sec,smooth)

#Loading density
delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,simulation,N_sec,smooth)

#Building data
os.system( "./Central_Voids_Properties.out %s %s %s %d"%( eigV_filename, delta_filename, "temp.tmp", b ) )

#Saving file
os.system( 'mv temp.tmp %scentral_void_cells_%s_b%d.dat'%(data_figures_fold,web,b) )