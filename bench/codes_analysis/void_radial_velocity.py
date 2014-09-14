#void_radial_velocity.py
#
#This code computes radial histograms of the velocity profile of voids as computed by the three 
#defined schemes
#
#Usage: run void_radial_velocity.py <Vweb or Tweb> <FAG or DLT> <Nth MF and BR>
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
bins = 20
#Number of times the effective radius of the void
Nreff = 2.0

#==================================================================================================
#			COMPUTING GEOMETRIC CENTER OF VOIDS
#==================================================================================================

print simulation

def Reff(X):
    return ((10**X*(0.9765625)**3)/( 4*np.pi/3. ))**(1/3.)

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
    
    #Number of cells
    N_data = int(voids[1, i_void -1 ])
    #Effective radius
    reff = Reff( np.log10(N_data) )
    #Geometric center
    cgc = GC[ i_void-1, 4: ]
    dist = [0,0,0]

    #Loading cells of the current void
    cells, rvel = Void_Velocity( "%s/%s/%s/%d/M"%\
    (foldglobal, simulation, "Vweb", N_sec), "%s/%s/%s/%d/P"%\
    (foldglobal, simulation, "Vweb", N_sec), cgc[0], cgc[1], cgc[2], int(Nreff*reff) )
    cells = np.transpose(cells)
          
    #Subdensitycenter
    csd = cells[np.argsort(rvel)[0]]
    cgc = csd
    
    #Radial Histogram
    hist = np.zeros( bins+1 )
    ncell = np.zeros( bins+1 )
    rbins = 10**np.linspace( np.log10(0.1), np.log10(Nreff*reff), bins+1 )

    #print i_void, reff
    for i_cell in xrange(len(cells)):
	for i_coor in xrange(3):
	    dist[i_coor] = abs(cells[i_cell,i_coor] - cgc[i_coor])
	    if dist[i_coor] >= N_sec: dist[i_coor] = N_sec - dist[i_coor]
	rdist = norm( dist )*L_box/(1.0*N_sec)+0.1
	rbin = int( (np.log10(rdist)- np.log10(0.1))*bins/(np.log10(Nreff*reff) - np.log10(0.1)) )
	if rbin <= bins:
	    ncell[rbin] += 1
	    hist[rbin] += rvel[ i_cell ]

    #Deleting empty regions
    rbins = rbins[ ncell!=0 ]
    hist = hist[ ncell!=0 ]
    ncell = ncell[ ncell!=0 ]
    
    np.savetxt( '%svoids_density_%s/%s/void_%d_VR.dat'%\
    (data_figures_fold,void_scheme,web,i_void-1), np.transpose([rbins, hist/ncell]), fmt = "%1.5e" )