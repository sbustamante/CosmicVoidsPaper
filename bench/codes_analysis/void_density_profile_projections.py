#void_density_profile_projections.py
#
#This code computes cartesian projections of the density profile of voids
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
N_cut = 2

#==================================================================================================
#			COMPUTING DENSITY PROFILES
#==================================================================================================

print simulation

#Loading the file with all the information about each region
voids = np.transpose( np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%1.2f/void_regions.dat"%\
(foldglobal, simulation, web, N_sec, void_scheme, Lambda_th )))

#Loading Density filename
delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,simulation,N_sec,smooth)

#Loading centres of each void
GC = np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%1.2f/GC.dat"%\
(foldglobal, simulation, web, N_sec, void_scheme, Lambda_th ))

#Sweeping throughout all regions
for i_void in voids[0]:
    sys.stdout.write( " In region:\t%d\r" %(int(i_void)) )
    sys.stdout.flush()
    #Loading cells of the current region
    region = np.transpose( np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%1.2f/void_%d.dat"%\
    (foldglobal, simulation, web, N_sec, void_scheme, Lambda_th, int(i_void) ))).astype(int)
  
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
	    e_inf = 0; e_sup = 0;
	    for i_sw in xrange(0,N_sec):
		if np.sum(region[axis,:] == i_sw)>0 and np.sum(region[axis,:] == i_sw+1)==0:
		    e_inf = i_sw
		if np.sum(region[axis,:] == N_sec-i_sw-1)>0 and np.sum(region[axis,:] == N_sec-i_sw-2)==0:
		    e_sup = N_sec-i_sw-1
		if e_inf !=0  and e_sup != 0:
		    break
	#Setting periodic boundaries (frac_reg>1, upper region denser, frac_reg<1, lower region denser)
	if First and Last:
	    frac_reg = np.sum( region[axis,:] >= N_sec/2. )/(1.0*np.sum( region[axis,:] < N_sec/2. ))
	    for i in xrange( N_data ):
		if region[axis,i] > e_inf and frac_reg<1:
		    region[axis,i] -= N_sec
		elif region[axis,i] <= e_sup and frac_reg>=1:
		    region[axis,i] += N_sec


	    
    #Sweeping all coordinates
    coord = [0,1,2,0,1]
    for axis in range( 3 ):
	#Current coordinate of geometric centre
	i_GC = GC[ i_void, axis+4 ].astype(int) - 1
	#Cutting density field in X direction
	delta = CutFieldZ( delta_filename, i_GC, 32, Coor = axis+1 )

	region_tm = region[ :, region[axis,:] == i_GC ]
	
	dimension = np.max( ( np.max(region_tm[coord[axis+1],:])-np.min(region_tm[coord[axis+1],:]), \
	np.max(region_tm[coord[axis+2],:])-np.min(region_tm[coord[axis+2],:]))  )
	
	print dimension