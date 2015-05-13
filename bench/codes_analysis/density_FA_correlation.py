#density_FA_correlation.py
#
#This code builds a matrix of correlations regarding FA field and delta value
#Usage: density_FA_correlation.py <Tweb or Vweb>
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
#Delta_min
delta_min = -0.999
#Delta_max
delta_max = 9
#N delta
N_delta = 100
#FA_min
FA_min = 0.0
#FA_max
FA_max = 1.0
#N delta
N_FA = 100

#Arrays
delta = 10**(np.linspace( np.log10(delta_min+1), np.log10(delta_max+1), N_delta ))-1
FA = np.linspace( FA_min, FA_max, N_FA )


#==================================================================================================
#			CONSTRUCTING MEDIANS OF DENSITY VS FA
#==================================================================================================

print simulation

#Loading eigenvalues
eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,simulation,web,N_sec,smooth)

#Loading density
delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,simulation,N_sec,smooth)

#Building the matrix      
delta_L1 = density_FA_correlation( eigV_filename, delta_filename, delta_min, delta_max, N_delta, FA_min, FA_max, N_FA )

#Initializing counters
Quartiles = np.zeros( (N_delta,4) )
for i_l in xrange( N_delta ):
      delta_L1[i_l,:] = np.cumsum( delta_L1[i_l,:] )
      delta_L1[i_l,:] /= delta_L1[i_l,-1]
      median = True
      Q1 = True
      Q3 = True
      Quartiles[i_l,0] = delta[i_l]
      for i_fa in xrange( N_delta ):
	  #Finding Median
	  if delta_L1[i_l,i_fa] > 0.5 and median:
	      median = False
	      Quartiles[i_l,2] = FA[i_fa]
	  #Finding Q1
	  if delta_L1[i_l,i_fa] > 0.25 and Q1:
	      Q1 = False
	      Quartiles[i_l,1] = FA[i_fa]
	  #Finding Q3
	  if delta_L1[i_l,i_fa] > 0.75 and Q3:
	      Q3 = False
	      Quartiles[i_l,3] = FA[i_fa]

np.savetxt( '%sFA_delta_%s.dat'%(data_figures_fold,web), Quartiles )

plt.fill_between( delta, Quartiles[:,1], Quartiles[:,3], alpha = 0.5 )
plt.plot( delta, Quartiles[:,2], "-" )
plt.show()