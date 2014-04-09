#voids_density_histogram.py
#
#This code calculates histograms of mean density for void regions according to Lambda_thr values
#Usage: voids_density_histogram.py
#
#by: Sebastian Bustamante

execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["BOLSHOI/"]
#Number of sections
N_sec = [256]
#Smooth parameter
smooth = '_s1'
#Web Scheme
webs = ['Vweb', 'Tweb']
#Styles
color = ['blue','green']

#N Lambda
N_l = 100
#Lambdas extremes values
L_min = 0
L_max = 2

#N delta
N_d = 100
#Delta extremes values
D_min = -1
D_max = 0


#==================================================================================================
#			CONSTRUCTING HISTOGRAMS
#==================================================================================================
N_sim = len(folds)

i_web = 0
for web in webs:
    i_fold = 0
    for fold in folds:
	print fold, web
	
	#Loading eigenvalues
	eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
	#Loading density
	delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,fold,N_sec[i_fold],smooth)
	#Calculating mean densities associated to differents kind of regions
	Voids_Histograms( eigV_filename, delta_filename, L_min, L_max, N_l, D_min, D_max, \
	N_d, '%svoids_delta_hist/%s'%(data_figures_fold,web) )
	print 'Histogram of mean density for voids, %s scheme: done!'%(web)

	i_fold += 1
    i_web += 1