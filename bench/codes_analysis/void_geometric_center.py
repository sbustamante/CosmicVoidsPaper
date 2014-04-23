#void_geometric_center.py
#
#This code computes the geometric center and the mass center of each void
#
#Usage: run void_geometric_center.py <Vweb or Tweb> <Lambda_th>
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
#Lambda_th
Lambda_th = float(sys.argv[2])
#Void finder scheme (FOF or LAY)
void_scheme = 'FOF'
#Cutt of respect to the number of cells
N_cut = 0

#==================================================================================================
#			COMPUTING GEOMETRIC CENTER OF VOIDS
#==================================================================================================

print simulation

#Loading the file with all the information about each region
voids = np.transpose( np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%1.2f/void_regions.dat"%\
(foldglobal, simulation, web, N_sec, void_scheme, Lambda_th )))

#Calculating geometric center
R_GCs = []
#Sweeping throughout all regions
for i_void in voids[0]:
    sys.stdout.write( " In region:\t%d\r" %(int(i_void)) )
    sys.stdout.flush()

    #Loading cells of the current region
    region = np.transpose( np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%1.2f/void_%d.dat"%\
    (foldglobal, simulation, web, N_sec, void_scheme, Lambda_th, int(i_void) )))
  
    #Cutt off respect to the number of cells
    N_data = len( region[0] )
    if N_data < N_cut:
	break

    #Standardizing periodic boundaries of X coordinates
    Last = False; First = False
    for i in xrange( N_data ):
	if region[0,i] == N_sec-1:	Last = True
	if region[0,i] == 0: 		First = True
	if First and Last:			break
    for i in xrange( N_data ):
	if region[0,i] >= N_sec/2. and First and Last:
	    region[0,i] -= N_sec
    #Standardizing periodic boundaries of Y coordinates
    Last = False; First = False
    for i in xrange( N_data ):
	if region[1,i] == N_sec-1:	Last = True
	if region[1,i] == 0: 		First = True
	if First and Last:			break
    for i in xrange( N_data ):
	if region[1,i] >= N_sec/2. and First and Last:
	    region[1,i] -= N_sec
    #Standardizing periodic boundaries of Z coordinates
    Last = False; First = False
    for i in xrange( N_data ):
	if region[2,i] == N_sec-1:	Last = True
	if region[2,i] == 0: 		First = True
	if First and Last:			break
    for i in xrange( N_data ):
	if region[2,i] >= N_sec/2. and First and Last: 
	    region[2,i] -= N_sec
	    
    #Geometric Center of this region 
    R_CM = np.zeros( 3 )
    for i in xrange( N_data ):
	R_CM[0] += region[0,i]
	R_CM[1] += region[1,i]
	R_CM[2] += region[2,i]
    R_CM *= L_box/( 1.0*N_data*N_sec )
    
    #Shifting values if they are outside the box volume of the simulation
    for i in xrange( 3 ):
	if R_CM[i] < 0:
	    R_CM[i] += L_box
    
    R_GCs.append( [i_void,R_CM[0],R_CM[1],R_CM[2]] )
    
R_GCs = np.array( R_GCs )

np.savetxt( "%s/%s/%s/%d/voids%s/voids_%1.2f/GC.dat"%\
(foldglobal, simulation, web, N_sec, void_scheme, Lambda_th ),R_GCs, fmt = "%d\t%1.5e\t%1.5e\t%1.5e" )