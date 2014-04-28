#FA_L1_correlation.py
#
#This code builds a matrix of correlations regarding FA and lambda_1 value
#Usage: FA_L1_correlation.py <Tweb or Vweb>
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
Lambda_max = 1
#N lambda
N_lamb = 100
#FA_min
FA_min = 0
#FA_max
FA_max = 1.0
#N FA
N_FA = 200

#Arrays
Lambda = np.linspace( Lambda_min, Lambda_max, N_lamb )
FA = np.linspace( FA_min, FA_max, N_FA )

#==================================================================================================
#			CONSTRUCTING MEDIANS OF FA REGARDING LAMBDA_1
#==================================================================================================

print simulation

#Loading eigenvalues
eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,simulation,web,N_sec,smooth)


#Building the matrix      
FA_L1 = FA_lambda1_correlation( eigV_filename, Lambda_min, Lambda_max, N_lamb, FA_min, FA_max, N_FA )

#Initializing counters
Quartiles = np.zeros( (N_lamb,3) )
for i_l in xrange( N_lamb ):
      FA_L1[i_l,:] = np.cumsum( FA_L1[i_l,:] )
      FA_L1[i_l,:] /= FA_L1[i_l,-1]
      median = True
      Q1 = True
      Q3 = True
      for i_fa in xrange( N_FA ):
	  #Finding Median
	  if FA_L1[i_l,i_fa] > 0.5 and median:
	      median = False
	      Quartiles[i_l,1] = FA[i_fa]
	  #Finding Q1
	  if FA_L1[i_l,i_fa] > 0.25 and Q1:
	      Q1 = False
	      Quartiles[i_l,0] = FA[i_fa]
	  #Finding Q3
	  if FA_L1[i_l,i_fa] > 0.75 and Q3:
	      Q3 = False
	      Quartiles[i_l,2] = FA[i_fa]

np.savetxt( '%sFA_L1_%s.dat'%(data_figures_fold,web), Quartiles )

plt.fill_between( Lambda, Quartiles[:,0], Quartiles[:,2], alpha = 0.5 )
plt.plot( Lambda, Quartiles[:,1], "-" )
plt.show()