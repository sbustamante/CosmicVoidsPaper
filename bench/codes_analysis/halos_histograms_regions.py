#halos_histogram_region.py
#
#This code calculates histograms of number of dark matter halos for each type of region, sweeping
#several lambda threshols values
#Usage: halos_histogram_region.py <BDM or FOF>
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
#Halo Scheme
catalog = sys.argv[1]
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
Lambda = np.linspace(L_min, L_max, N_l)


#==================================================================================================
#			CONSTRUCTING HISTOGRAMS
#==================================================================================================
i_web = 0
for web in webs:
    #Number of dark matter halos per region
    Numb_GH = np.zeros( (N_l,5) )
    print simulation, web
    
    #Loading eigenvalues
    eigV = np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,simulation,web,N_sec,smooth,catalog))

    for i_l in xrange( N_l ):
	lamb = Lambda[i_l]
	#Storing lambda value
	Numb_GH[i_l,0] = lamb
	#Halos in Voids
	bool_v = (eigV[:,1] <= lamb)*(eigV[:,2] <= lamb)*(eigV[:,3] <= lamb)
	Numb_GH[i_l,1] = len( eigV[bool_v,0] )/(1.0*len( eigV ))
	#Halos in Sheets
	bool_s = (eigV[:,1] > lamb)*(eigV[:,2] <= lamb)*(eigV[:,3] <= lamb)
	Numb_GH[i_l,2] = len( eigV[bool_s,0] )/(1.0*len( eigV ))
	#Halos in Filaments
	bool_f = (eigV[:,1] > lamb)*(eigV[:,2] > lamb)*(eigV[:,3] <= lamb)
	Numb_GH[i_l,3] = len( eigV[bool_f,0] )/(1.0*len( eigV ))
	#Halos in Knots
	bool_k = (eigV[:,1] > lamb)*(eigV[:,2] > lamb)*(eigV[:,3] > lamb)
	Numb_GH[i_l,4] = len( eigV[bool_k,0] )/(1.0*len( eigV ))
		
    np.savetxt( '%shalos_count_regions_%s_%s.dat'%(data_figures_fold,catalog,web),\
    Numb_GH, fmt="%1.5e\t\t%1.5e\t%1.5e\t%1.5e\t%1.5e" )
    
    i_web += 1