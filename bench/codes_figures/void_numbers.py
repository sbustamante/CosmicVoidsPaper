#void_numbers.py
#
#This code computes the number of voids per bin for over and subcompensated voids
#
#Usage: void_numbers.py <Vweb or Tweb> <FAG or DLT> <undercomp(0) overcomp(1)> 
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
#Void finder scheme (FAG or DLG)
void_scheme = sys.argv[2]
#Cutt of respect to the number of cells
N_cut = 2
#Configuration 
config = "01"
#Compensated
comp = int(sys.argv[3])

#Number of middle points for mapping the density field
N = 80
#Number of times the effective radius of the void
Rreff = 8
#Effective radial bins 
RadBins = [ 0.0, 2.0, 3.2, 4.4, 5.6, 6.8, 8.3, 12, 100.0 ]

#Effective radius function
def r_eff(X):
    return ((10**np.log10(X)*(0.9765625)**3)/( 4*np.pi/3. ))**(1/3.)

#==================================================================================================
#			COMPUTING RADIAL PROFILES OF DENSITY FOR EVERY RADIAL BIN
#==================================================================================================
fig = plt.figure( figsize=(5.8,5) )
ax = fig.add_subplot(111)

Total = 0
for ri in xrange( len(RadBins)-1 ):
    reff_range = [ RadBins[ri],RadBins[ri+1] ]
    #Loading index of voids
    voids = np.loadtxt("%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%\
    (foldglobal, simulation, web, N_sec, void_scheme, config ))
    #Loading compensated
    compensated = np.loadtxt("%s/%s/%s/%d/voids%s/voids_%s/comp_half.dat"%\
    (foldglobal, simulation, web, N_sec, void_scheme, config ))
  
    indexes = voids[ (reff_range[0]<=r_eff(voids[:,1])) & (r_eff(voids[:,1])<reff_range[1]) & ( compensated[:,1] == comp ) ,0 ]
    print "Bins:", reff_range, "Number:", len(indexes)
    Total+=len(indexes)
print "TOTAL:", Total    
