#void_geometric_center.py
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

#Calculating geometric center
R_GCs = []
#Sweeping throughout all regions
for i_void in voids[0]:
    sys.stdout.write( " In region:\t%d\r" %(int(i_void)) )
    sys.stdout.flush()

    #Loading cells of the current region
    region = np.transpose( np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%s/void_%d.dat"%\
    (foldglobal, simulation, web, N_sec, void_scheme, config, int(i_void) )))
  
    #Cutt off respect to the number of cells
    try:
      N_data = len( region[0] )
    except:
      N_data = 1
    if N_data < N_cut:
	break

    #Standardizing periodic boundaries ------------------------------------------------------------
    for axis in range( 3 ):
	Last = False; First = False
	for i in xrange( N_data ):
	    if region[axis,i] == N_sec-1:	Last = True
	    if region[axis,i] == 0: 		First = True
	    if First and Last:			break
	    
	#Identifying two extreme positions
	if First and Last:
	    e_inf = -1; e_sup = -1;
	    for i_sw in xrange(0,N_sec):
		if np.sum(region[axis,:] == i_sw)>0 and np.sum(region[axis,:] == i_sw+1)==0:
		    e_inf = i_sw
		if np.sum(region[axis,:] == N_sec-i_sw-1)>0 and np.sum(region[axis,:] == N_sec-i_sw-2)==0:
		    e_sup = N_sec-i_sw-1
		if e_inf != -1  and e_sup != -1:
		    break
	#Setting periodic boundaries (frac_reg>1, upper region denser, frac_reg<1, lower region denser)
	if First and Last:
	    frac_reg = np.sum( region[axis,:] > N_sec/2. )/(1.0*np.sum( region[axis,:] <= N_sec/2. ))
	    for i in xrange( N_data ):
		if region[axis,i] > e_inf and frac_reg<1:
		    region[axis,i] -= N_sec
		elif region[axis,i] < e_sup and frac_reg>=1:
		    region[axis,i] += N_sec
	    
    #Geometric Center of this region 
    C_CM = np.array( [np.mean(region[0,:]), np.mean(region[1,:]), np.mean(region[2,:]) ] )
    R_CM = C_CM*L_box/( 1.0*N_sec )
    C_CM = C_CM.astype(int)
    
    
    #Shifting values if they are outside the box volume of the simulation
    for i in xrange( 3 ):
	if R_CM[i] < 0:
	    R_CM[i] += L_box
	    C_CM[i] += N_sec
	if R_CM[i] > N_sec:
	    R_CM[i] -= L_box
	    C_CM[i] -= N_sec
    
    R_GCs.append( [i_void,R_CM[0],R_CM[1],R_CM[2],C_CM[0],C_CM[1],C_CM[2]] )

R_GCs = np.array( R_GCs )

np.savetxt( "%s/%s/%s/%d/voids%s/voids_%s/GC.dat"%\
(foldglobal, simulation, web, N_sec, void_scheme, config ),R_GCs, fmt = "%d\t%1.5e\t%1.5e\t%1.5e\t%d\t%d\t%d" )