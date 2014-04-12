#density_histogram_filaments.py
#
#This code calculates histograms of mean density for filament regions according to Lambda_thr values
#Usage: density_histogram_filaments.py <Compute histograms(0), Only quartiles(1)>
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
webs = ['Vweb', 'Tweb']
#Styles
color = ['blue','green']

#N Lambda
N_l = 100
#Lambdas extremes values
L_min = 0
L_max = 1
#Lambda array
Lambda = np.linspace(L_min, L_max, N_l+1)

#N delta
N_d = 4000
#Delta extremes values
D_min = -1
D_max = 20

#Uncertain of quartiles
Delta_Q = 0.005

#==================================================================================================
#			CONSTRUCTING HISTOGRAMS
#==================================================================================================
i_web = 0
for web in webs:
    #Quartiles array
    Quart = np.zeros( (N_l-1,4) )
    print simulation, web
    
    if sys.argv[1] == "0":
	#Loading eigenvalues
	eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,simulation,web,N_sec,smooth)
	#Loading density
	delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,simulation,N_sec,smooth)
	#Calculating mean densities associated to differents kind of regions
	Regions_Histograms( eigV_filename, delta_filename, L_min, L_max, N_l, D_min, D_max, \
	N_d, 2, '%sfilaments_delta_hist/%s'%(data_figures_fold,web) )
	print 'Histogram of mean density for filaments, %s scheme: done!'%(web)
    
    for i_l in xrange( N_l-1 ):
	lamb = Lambda[i_l]
	hist_filaments = np.loadtxt( '%sfilaments_delta_hist/%s/delta_filaments_hist_%1.2f.dat'%(data_figures_fold,web,lamb) )
	for i_d in range( N_d-1 ):
	    Quart[i_l,0] = lamb
	    #Q1
	    if 0.25 - Delta_Q <= hist_filaments[i_d,2]/hist_filaments[-1,2] <= 0.25 + Delta_Q:
		Quart[i_l,1] = hist_filaments[i_d,0]
	    #Median
	    elif 0.50 - Delta_Q <= hist_filaments[i_d,2]/hist_filaments[-1,2] <= 0.50 + Delta_Q:
		Quart[i_l,2] = hist_filaments[i_d,0]
	    #Q3
	    elif 0.75 - Delta_Q <= hist_filaments[i_d,2]/hist_filaments[-1,2] <= 0.75 + Delta_Q:
		Quart[i_l,3] = hist_filaments[i_d,0]
		
    np.savetxt( '%sfilaments_delta_hist/%s/quartiles.dat'%(data_figures_fold,web), Quart )
    
    i_web += 1