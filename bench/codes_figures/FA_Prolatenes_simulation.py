#FA_Prolatenes_simulation.py
#
#This code performs an scatter plot of the FA and the Prolatenes index for random samples of the
#simulation
#Usage FA_Prolatenes_MonteCarlo.py <Tweb or Vweb> <0-Show  1-Save>
#
#by: Sebastian Bustamante

execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
simulation = "BOLSHOI/"
#Labels of graphs
labels = "BOLSHOI"
#Box lenght
Box_L = 250
#Number of sections
N_sec = 256
#Web scheme
web = sys.argv[1]
#Values to evaluate lambda_th
Lambda_opt = 0
#Smooth parameter
smooth = '_s1'
#Coordinate to cut (1 -- X, 2 -- Y, 3 -- Z)
axe = 1
#Cut
Cuts = [10, 50, 100, 150]
#Lambda_th
Lth = { "Tweb":0.265, "Vweb":0.175 }
#Colors
colors = ["navy", "yellowgreen", "orangered", "c"]
#colors = ["red", "blue", "green", "gray"]
#Labels
labels = ["voids", "sheets", "filaments", "knots"]

#==================================================================================================
#			PLOTING WEB SCHEME AND DENSITY FIELD FOR SIMULATION
#==================================================================================================
fig = plt.figure( figsize=(7,7) )

#Loading Density filename
delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,simulation,N_sec,smooth)
#Loading Vweb filename
eig_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,simulation,web,N_sec,smooth)

for Cut in Cuts:
    #Loading Fields
    delta = CutFieldZ( delta_filename, Cut, 32, Coor = axe )
    eig1 = CutFieldZ( eig_filename+"_1", Cut, 16, Coor = axe )
    eig2 = CutFieldZ( eig_filename+"_2", Cut, 16, Coor = axe )
    eig3 = CutFieldZ( eig_filename+"_3", Cut, 16, Coor = axe )

    eigT = sqrt( eig1**2+eig2**3+eig3**2 )

    sch = Scheme(eig1, eig2, eig3, Lth[web])
    p = Prolatenes(eig1/eigT, eig2/eigT, eig3/eigT)
    fa = Fractional_Anisotropy(eig1, eig2, eig3)

    Npoints = np.min( [len(sch[sch==i]) for i in xrange(4)] )

    #Plotting each type of environment
    for i in xrange(4):
	if Cut == Cuts[-1]:
	    plt.plot( p[sch==i][:Npoints], fa[sch==i][:Npoints], '.', color = colors[i], label = labels[i], markersize=3.5 )
	else:
	    plt.plot( p[sch==i][:Npoints], fa[sch==i][:Npoints], '.', color = colors[i], markersize=3.5 )
	
plt.xlim( -1.2, 1.2 )
plt.ylim( 0, 1 )
plt.legend( loc='lower right', fancybox = True, shadow = True, ncol = 1, prop={'size':12} )
plt.xlabel( "Prolatenes" )
plt.ylabel( "Fractional Anisotropy" )
plt.hlines( 0.95, -1.2, 1.2, color="black", linewidth = 1.5, zorder = 100 )
plt.subplots_adjust( top = 0.96, right = 0.99, bottom = 0.06, left = 0.08 )
plt.grid(1)
if sys.argv[2] == '1':
    plt.savefig( '%sFA_Prolatenes_%s.pdf'%(figures_fold, web) )
else:
    plt.show()