#void_radial_density.py
#
#This code computes radial histograms of the density profile of voids as computed by the three 
#defined schemes
#
#Usage: run void_radial_density.py <Vweb or Tweb> <FAG or DLT> <Nth MF and BR>
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

#Bins of histogram of radius
bins = 100
#Number of times the effective radius of the void
Nreff = 6

#Bins of histogram of radius
Dbins = 5
#Minimum delta
Dlmin = -1
#Maximum delta
Dlmax = 4

#Interval of radius [Mpc]
Rmin = 1
Rmax = 14
Nint = 13



#==================================================================================================
#DIRECT METHOD USING C
#==================================================================================================
filename_delta = "%s/%s/%s/%d/Delta%s"%(foldglobal, simulation, web, N_sec, smooth)
out_folder = "%svoids_density_%s/bins_%s"%(data_figures_fold,void_scheme,web)
indexes = "%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%(foldglobal, simulation, web, N_sec, void_scheme, config )
CM = "%s/%s/%s/%d/voids%s/voids_%s/GC.dat"%(foldglobal, simulation, web, N_sec, void_scheme, config )

os.system( "rm Void_Density_Bins.out" )
os.system( "make Void_Density_Bins" )
os.system( "./Void_Density_Bins.out %s %s %s %s %d %d %f %f %d %f %d %d"%\
( filename_delta, out_folder, indexes, CM, bins, Nreff, Rmin, Rmax, Nint, Dlmin, Dlmax, Dbins ) )