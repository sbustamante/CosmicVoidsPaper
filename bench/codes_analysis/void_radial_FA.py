#void_radial_density.py
#
#This code computes radial histograms of the FA profile of voids as computed by the three 
#defined schemes
#
#Usage: run void_radial_FA.py <Vweb or Tweb> <FAG or DLT> <Nth MF and BR>
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
#Box lenght [Mpc]
L_box = 250.
#Smooth parameter
smooth = '_s1'
#Web Scheme
web = sys.argv[1]
#Config
config = sys.argv[3]
#Void finder scheme (FAG or DLG)
void_scheme = sys.argv[2]
#Cutt of respect to the number of cells
N_cut = 2

#Bins of histogram
bins = 80
#Number of times the effective radius of the void
Nreff = 8

    
###################################################################################################
#DIRECT METHOD USING C
###################################################################################################
filename_eig = "%s/%s/%s/%d/Eigen%s"%(foldglobal, simulation, web, N_sec, smooth)
out_folder = "%svoids_density_%s/%s"%(data_figures_fold,void_scheme,web)
indexes = "%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%(foldglobal, simulation, web, N_sec, void_scheme, config )
#CM = "%s/%s/%s/%d/voids%s/voids_%s/GC.dat"%(foldglobal, simulation, web, N_sec, void_scheme, config )
CM = "%s/%s/%s/%d/voids%s/voids_%s/DC.dat"%(foldglobal, simulation, web, N_sec, void_scheme, config )

os.system( "rm Void_FA_All.out" )
os.system( "make Void_FA_All" )
os.system( "./Void_FA_All.out %s %s %s %s %d %d"%( filename_eig, out_folder, indexes, CM, bins, Nreff ) )