#FA_histograms.py
#
#This code builds an histogram of all cells in the simulation classified into four different regions
#and store the abundances for each range of FA
#Usage: FA_histograms.py <Tweb or Vweb>
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
#Web Scheme
web = sys.argv[1]
#Smooth parameter
smooth = '_s1'
#Range of FA
FA_min = 0
FA_max = 1.05
#Number of bins
N_FA = 200
FAs = np.linspace( FA_min, FA_max, N_FA + 1 )

#Values to evaluate lambda_th
if web == 'Tweb':
    Lambda = 0.265
if web == 'Vweb':
    Lambda = 0.175
    
#==================================================================================================
#			CONSTRUCTING MEDIANS OF DENSITY REGARDING LAMBDA_1
#==================================================================================================

print simulation

#Eigenvector web filename
eig_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,simulation,web,N_sec,smooth)

#Loading eigenvectors
eig1 = read_CIC_scalar( eig_filename+"_1" )
eig1 = eig1.flatten()
eig2 = read_CIC_scalar( eig_filename+"_2" )
eig2 = eig2.flatten()
eig3 = read_CIC_scalar( eig_filename+"_3" )
eig3 = eig3.flatten()

#Calculating FA
FA = Fractional_Anisotropy( eig1, eig2, eig3 )

#Calculating scheme
scheme = Scheme_flatten( eig1, eig2, eig3, Lambda )

#Initializing histograms
FA_hist = np.zeros( (N_FA,5) )
FA_hist[:,0] = FAs[:-1]
for i_fa in xrange(N_FA):
    for env in xrange(4):
	FA_hist[i_fa,env+1] = (( FA[scheme==env]>=FAs[i_fa] )&( FA[scheme==env]<FAs[i_fa+1] )).sum()

np.savetxt( '%sFA_Environment_%s.dat'%(data_figures_fold,web), FA_hist )