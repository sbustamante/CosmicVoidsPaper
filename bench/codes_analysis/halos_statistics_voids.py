#halos_statistics_voids.py
#
#This code calculates statistics of some discrete properties associated to dark matter halos in 
#voids (lambda_1 eigenvalue)
#Usage: halos_mass_environment.py <BDM or FOF>
#
#by: Sebastian Bustamante

execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
simulation = "BOLSHOI/"
#Grid resolution (size)
N_box = 256
#Lenght of the simulation box
L_box = 250.0
#Smooth parameter
smooth = '_s1'
#Halo Scheme
catalog = sys.argv[1]
#Web Scheme
web = ["Tweb", "Vweb"]


#N Lambda_1
N_l = 100
#Lambdas extremes values
L_min = -0.3
L_max = 2.0
#Lambda array
Lambda_1 = np.linspace( L_min, L_max, N_l+1 )
L1_Halos_T = np.zeros(N_l+1)
L1_Halos_V = np.zeros(N_l+1)

#==================================================================================================
#			CONSTRUCTING HISTOGRAMS
#==================================================================================================
#Loading general catalog of halos
GH = np.loadtxt('%s%sC_GH_%s.dat'%(foldglobal,simulation,catalog))

#Loading eigenvalues
eigT = np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,simulation,web[0],N_box,smooth,catalog))
eigV = np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,simulation,web[1],N_box,smooth,catalog))

for i_h in xrange( len(GH) ):
    #Tweb
    i_lT = np.floor((eigT[i_h,1]-L_min/( L_max-L_min ))*N_l)
    if 0 <= i_lT <= N_l:
	L1_Halos_T[i_lT] += 1
    #Vweb
    i_lV = np.floor((eigV[i_h,1]-L_min/( L_max-L_min ))*N_l)
    if 0 <= i_lV <= N_l:
	L1_Halos_V[i_lV] += 1
    
    
    
plt.plot( Lambda_1, L1_Halos_V, Lambda_1, L1_Halos_T, "-" ); plt.show()


  