#density_L1_correlation.py
#
#This code builds a matrix of correlations regarding density field and lambda_1 value
#Usage: density_L1_correlation.py <Tweb or Vweb>
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
#Smooth parameter
smooth = '_s1'
#Web Scheme
web = sys.argv[1]
#Lambda_min
Lambda_min = -1
#Lambda_max
Lambda_max = 5
#N lambda
N_lamb = 200
#Delta_min
delta_min = -1.0
#Delta_max
delta_max = 1.0
#N delta
N_delta = 200

#Arrays
Lambda = np.linspace( Lambda_min, Lambda_max, N_lamb )
delta = np.linspace( delta_min, delta_max, N_delta )

#==================================================================================================
#			CONSTRUCTING MEDIANS OF DENSITY REGARDING LAMBDA_1
#==================================================================================================

print simulation

#Loading eigenvalues
eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,simulation,web,N_sec,smooth)

#Loading density
delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,simulation,N_sec,smooth)

#Building the matrix      
delta_L1 = density_lambda1_correlation( eigV_filename, delta_filename, Lambda_min, Lambda_max, N_lamb, delta_min, delta_max, N_delta )

#Initializing counters
Quartiles = np.zeros( (N_lamb,4) )
for i_l in xrange( N_lamb ):
      delta_L1[i_l,:] = np.cumsum( delta_L1[i_l,:] )
      delta_L1[i_l,:] /= delta_L1[i_l,-1]
      median = True
      Q1 = True
      Q3 = True
      Quartiles[i_l,0] = Lambda[i_l]
      for i_fa in xrange( N_delta ):
	  #Finding Median
	  if delta_L1[i_l,i_fa] > 0.5 and median:
	      median = False
	      Quartiles[i_l,2] = delta[i_fa]
	  #Finding Q1
	  if delta_L1[i_l,i_fa] > 0.25 and Q1:
	      Q1 = False
	      Quartiles[i_l,1] = delta[i_fa]
	  #Finding Q3
	  if delta_L1[i_l,i_fa] > 0.75 and Q3:
	      Q3 = False
	      Quartiles[i_l,3] = delta[i_fa]

#np.savetxt( '%sdelta_L1_%s.dat'%(data_figures_fold,web), Quartiles )

plt.fill_between( Lambda, Quartiles[:,1], Quartiles[:,3], alpha = 0.5 )
plt.plot( Lambda, Quartiles[:,2], "-" )
plt.show()