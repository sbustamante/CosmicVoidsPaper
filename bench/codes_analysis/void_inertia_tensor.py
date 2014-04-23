#void_intertia_tensor.py
#
#This code computes the reduced intertia tensor of each void region found by the FOF scheme. For 
#each region is also computed the associated eigenvalues and the principal directions of inertia 
#in order to quantify the shape of those regions.
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
#Catalog Scheme
catalog = 'FOF'
#Web Scheme
web = 'Vweb'
#Lambda_th
Lambda_th = 0.0
#Void finder scheme (FOF or LAY)
void_scheme = 'FOF'
#Cutt of respect to the number of cells
N_cut = 8

#==================================================================================================
#			COMPUTING EIGENVALUES AND BUILDING THE INERTIA TENSOR
#==================================================================================================

print simulation

#Loading the file with all the information about each region
voids = np.transpose( np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%1.2f/void_regions.dat"%\
(foldglobal, simulation, web, N_sec, void_scheme, Lambda_th )))

#Calculating eigenvalues and principal directions of inertia
Eigenvalues = []
Eigenvector = []
#Sweeping through the regions
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
	    
    #Center of mass of this region 
    R_CM = np.zeros( 3 )
    for i in xrange( N_data ):
	R_CM[0] += region[0,i]
	R_CM[1] += region[1,i]
	R_CM[2] += region[2,i]
    R_CM *= L_box/( 1.0*N_data*N_sec )
    
    #Inertia tensor
    tensor = np.zeros( (3,3) )
    for i in xrange( N_data ):
	r = np.zeros( 3 )
	r[0] = region[0,i]*L_box/( 1.0*N_sec ) - R_CM[0]
	r[1] = region[1,i]*L_box/( 1.0*N_sec ) - R_CM[1]
	r[2] = region[2,i]*L_box/( 1.0*N_sec ) - R_CM[2]
	Rl2 = r[0]**2 + r[1]**2 + r[2]**2
	for ii in xrange(3):
	    for jj in xrange(3):
		tensor[ii,jj] += (r[ii]*r[jj])/Rl2
	
    eigs = np.linalg.eig( tensor )
    Eigenvalues.append( np.sort( eigs[0] ) )
    Eigenvector.append( eigs[1][ np.argsort( eigs[0] ) ].flatten() )

Eigenvalues = np.array( Eigenvalues )
Eigenvector = np.array( Eigenvector )

np.savetxt( "%s/%s/%s/%d/voids%s/voids_%1.2f/eigen.dat"%\
(foldglobal, simulation, web, N_sec, void_scheme, Lambda_th ),\
np.transpose(np.concatenate( (Eigenvalues.T, Eigenvector.T) )),\
fmt = "%1.5e\t%1.5e\t%1.5e\t%1.5e\t%1.5e\t%1.5e\t%1.5e\t%1.5e\t%1.5e\t%1.5e\t%1.5e\t%1.5e" )