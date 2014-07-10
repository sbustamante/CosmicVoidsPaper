#void_radial_density.py
#
#This code computes the geometric center and the mass center of each void
#
#Usage: run void_geometric_center.py <Vweb or Tweb> <FAG or DLT> <Nth MF and BR>
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
#Void finder scheme (FOF or LAY)
void_scheme = sys.argv[2]
#Cutt of respect to the number of cells
N_cut = 2

#==================================================================================================
#			COMPUTING GEOMETRIC CENTER OF VOIDS
#==================================================================================================

print simulation

#Loading the file with all the information about each region
voids = np.transpose( np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%\
(foldglobal, simulation, web, N_sec, void_scheme, config )))

#Loading centres of each void
GC = np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%s/GC.dat"%\
(foldglobal, simulation, web, N_sec, void_scheme, config ))
  
#Sweeping throughout all regions
for i_void in voids[0]:
    sys.stdout.write( " In region:\t%d\r" %(int(i_void)) )
    sys.stdout.flush()

    #Loading cells of the current void
    cells = np.transpose( np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%s/void_%d.dat"%\
    (foldglobal, simulation, web, N_sec, void_scheme, config, int(i_void) )))
  
    #Loading densities of the current void
    rhos = np.transpose( np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%s/void_%d_rho.dat"%\
    (foldglobal, simulation, web, N_sec, void_scheme, config, int(i_void) )))
    
    #Cutt off respect to the number of cells
    try:
      N_data = len( region[0] )
    except:
      N_data = 1
    if N_data < N_cut:
	break

    


    #np.savetxt( '%svoids_density_%s/%s/void_%d_DR.dat'%\
    #(data_figures_fold,void_scheme,web,i_void), density.flatten(), fmt = "%1.3e" )