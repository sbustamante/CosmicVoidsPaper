#void_compensantion.py
#
#This code classifies voids into overcompensated and undercompensated voids.
#
#Usage: run void_compensantion.py <Vweb or Tweb> <FAG or DLT> <Nth MF and BR>
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

#==================================================================================================
#			COMPUTING RADIAL PROFILES OF DENSITY FOR EVERY RADIAL BIN
#==================================================================================================
plt.figure( figsize=(5.5,5) )
#Loading index of voids
voids = np.loadtxt("%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%\
(foldglobal, simulation, web, N_sec, void_scheme, config ))

comps = []
#Sweeping voids
for iv in xrange(int(voids[-1,0])):
    #Loading profiles
    rprofile = np.loadtxt('%svoids_density_%s/%s/void_%d_DR.dat'%(data_figures_fold,void_scheme,web,iv))
    #Density
    rho = rprofile[:,1]+1
    #Normed Radius
    ur = rprofile[ np.isnan(rho)==False ,0]
    #Deleting nans
    rho = rho[ np.isnan(rho)==False ]
    #Interpolating
    rho_interp = interp.interp1d( ur, rho )
    #Integrating mass deviation
    comps.append( int(integ.quad( lambda r: rho_interp(r)*r**2, ur.min(), 4.0 )[0]/(4.0**3-ur.min()**3)*3.0) )
    print "In void:", iv

np.savetxt("%s/%s/%s/%d/voids%s/voids_%s/comp.dat"%\
(foldglobal, simulation, web, N_sec, void_scheme, config ), np.transpose([ list(voids[:,0]),comps ]), fmt = "%d\t%d" ) 