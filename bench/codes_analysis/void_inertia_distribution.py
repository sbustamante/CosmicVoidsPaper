#void_intertia_tensor.py
#
#This code computes distributions of the eigenvalues of the reduced intertia tensor of each void 
#region found by the FOF scheme. The eigenvalues were sorted such as Lambda1 < Lambda2 < Lambda3.
#Here it will be calculated non-integrated and normed distributions of Lambda1/Lambda2 and 
#Lambda1/Lambda3 in order to determinate the shape of void regions.
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
#Box lenght [Mpc]
L_box = [250.]
#Smooth parameter
smooth = '_s1'
#Web Scheme
web = 'Tweb'
#Lambda_th
Lambda_th = 0.0
#Nbins of each histogram
Nbins = 10

#==================================================================================================
#			COMPUTING EIGENVALUES AND BUILDING THE INERTIA TENSOR
#==================================================================================================

i_fold = 0
N_sim = len(folds)

#no labels
nullfmt = NullFormatter()

#definitions for the axes
left, width = 0.1, 0.65
bottom_v, height = 0.1, 0.65
bottom_h = left_h = left+width+0.02

rect_hist2D = [left, bottom_v, width, height]
rect_histx = [left, bottom_h, 1.335*width, 0.2]
rect_histy = [left_h, bottom_v, 0.2, height]

#start with a rectangular Figure
plt.figure(1, figsize=(8,8))

axHist2D = plt.axes(rect_hist2D)
axHistx = plt.axes(rect_histx)
axHisty = plt.axes(rect_histy)

#no labels
axHistx.xaxis.set_major_formatter(nullfmt)
axHisty.yaxis.set_major_formatter(nullfmt)


for fold in folds:
    print fold
    
    
    eigen = np.transpose(np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%1.2f/eigen.dat"%\
    (foldglobal, fold, web, N_sec[i_fold], smooth, Lambda_th )))
  
    Hist_lambd  = np.transpose(np.histogram2d( eigen[0]/eigen[1], eigen[1]/eigen[2], 
    bins = Nbins, normed = False, range = ((0,1),(0,1))  )[0][::,::-1])
    
    #2D histogram
    map2d = axHist2D.imshow( Hist_lambd[::,::], interpolation='nearest', aspect = 'auto',
    cmap = 'binary', extent = (0,1,0,1) )	
    #Create the colorbar
    axc, kw = matplotlib.colorbar.make_axes( axHistx,\
    orientation = "vertical", shrink=1., pad=.1, aspect=10 )
    cb = matplotlib.colorbar.Colorbar( axc, map2d,\
    orientation = "vertical" )
    #Set the colorbar
    map2d.colorbar = cb
   
    #Countorn
    axHist2D.contour( Hist_lambd[::-1,::], 7, aspect = 'auto', 
    extent = (0,1,0,1),linewidth=1.5, interpolation = 'gaussian',\
    colors="black" )
    
    #Histogram X
    histx = np.histogram( eigen[0]/eigen[1], bins=Nbins, normed=True, range=(0,1) )
    axHistx.bar( histx[1][:-1], histx[0], width = 1.00/Nbins, linewidth=2.0, color="gray" )
    #Histogram Y
    histy = np.histogram( eigen[1]/eigen[2], bins=Nbins, normed=True, range=(0,1) )
    axHisty.barh( histy[1][:-1], histy[0], height = 1.00/Nbins, linewidth=2.0, color="gray" )
  
      
    i_fold += 1

axHistx.set_xlim( axHist2D.get_xlim() )
axHistx.set_xticks( np.linspace( 0,1,Nbins+1 ) )
axHistx.grid( color='black', linestyle='--', linewidth=1., alpha=0.3 )
axHistx.set_ylabel( "Normed distribution" )

axHisty.set_ylim( axHist2D.get_ylim() )
axHisty.set_yticks( np.linspace( 0,1,Nbins+1 ) )
axHisty.grid( color='black', linestyle='--', linewidth=1., alpha=0.3 )
axHisty.set_xlabel( "Normed distribution" )

axHist2D.grid( color='black', linestyle='--', linewidth=1., alpha=0.3 )
axHist2D.set_xticks( np.linspace( 0,1,Nbins+1 ) )
axHist2D.set_yticks( np.linspace( 0,1,Nbins+1 ) )
axHist2D.set_xlabel( "$\\tau_1/\\tau_2$", fontsize=15 )
axHist2D.set_ylabel( "$\\tau_2/\\tau_3$", fontsize=15 )

axHist2D.hlines( 0.7, 0.0, 0.7, linestyle="--", color="red", linewidth=2.5 )
axHist2D.text( 0.35, 0.81, "Pancake\nvoids", fontweight="bold", color="red",\
fontsize=15, horizontalalignment="center" )

axHist2D.vlines( 0.7, 0.0, 0.7, linestyle="--", color="green", linewidth=2.5 )
axHist2D.text( 0.85, 0.3, "Filamentary\nvoids", fontweight="bold", color="green",\
fontsize=15, horizontalalignment="center" )

axHist2D.hlines( 0.7, 0.7, 1.0, linestyle="--", color="blue", linewidth=2.5 )
axHist2D.vlines( 0.7, 0.7, 1.0, linestyle="--", color="blue", linewidth=2.5 )
axHist2D.text( 0.85, 0.81, "Isotropic\nvoids", fontweight="bold", color="blue",\
fontsize=15, horizontalalignment="center" )
axHist2D.text( 0.35, 0.3, "Anisotropic\nvoids", fontweight="bold", color="black",\
fontsize=15, horizontalalignment="center" )

axHist2D.text( 0.01, 0.01, "%s"%(web), fontweight="bold", color="black",\
fontsize=15 )

plt.show()