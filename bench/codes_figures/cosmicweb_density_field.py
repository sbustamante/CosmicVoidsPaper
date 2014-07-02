#cosmicweb_density_field.py
#
#This code perform a graphic scheme of the visual impresion for a defined cutting off of Bolshoi
#simulation, using the density field it is performed a classification scheme of voids based upon
#cuts of the density.
#Usage cosmicweb_density_field.py <catalogue, BDM or FOF> <show(0) or save(1)> <format (png, pdf)>
#
#by: Sebastian Bustamante

execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
simulation = "BOLSHOI/"
#Box lenght
Box_L = 250
#Number of sections
N_sec = 256

#Halo Scheme
catalog = sys.argv[1]

#Void catalogue
void_scheme = "DLG"
#Void parameters ( Nth-order median filtering,  Boolean for boundary removals )
config = "51"
#Smooth parameter
smooth = '_s1'
#Coordinate to cut (1 -- X, 2 -- Y, 3 -- Z)
axe = 1
#Cut
Cut = 200
#Halos slice cut [Mpc]
dx = 2

#Colors
my_cmapC = plt.cm.get_cmap('gray')
my_cmap4 = plt.cm.get_cmap('gray', 4)

from matplotlib.colors import colorConverter
cmap2 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap2',["black","white"],2)
cmap2._init()
alphas = np.ones( cmap2.N+3)
alphas[0] = 0
cmap2._lut[:,-1] = alphas

#==================================================================================================
#			PLOTING WEB SCHEME AND DENSITY FIELD FOR SIMULATION
#==================================================================================================
'''
FIGURE SCHEME
-------------------
|  1  |  2  |  3  |
-------------------
'''
plt.figure( figsize=(18,7) )
plt.subplots_adjust( top=0.93, bottom = 0.07, right = .98, left = 0.04, hspace = 0.14, wspace=0.08 )
#Extent
extent = [0, Box_L, 0, Box_L]

#Loading Density filename
delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,simulation,N_sec,smooth)
#Loading general catalog of halos
GH = np.loadtxt('%s%sC_GH_%s.dat'%(foldglobal,simulation,catalog))
#Catalogue of voids
voids = CutFieldZ( "%s/%s/%s/%d/voids%s/voids_%s/void_index.dat"%\
(foldglobal, simulation, "Tweb", N_sec, void_scheme, config ), Cut, 'plain', Coor = axe )
#Loading Fields
delta = CutFieldZ( delta_filename, Cut, 32, Coor = axe )


#FA field
plt.subplot( 1, 3, 1 )
plt.imshow( np.transpose(np.log( delta + 1 )[::,::-1]), extent = extent, cmap = "binary" )
#plt.contour( np.transpose(delta), levels=[-0.57], extent = extent, linestyles="-",\
#colors=[(0.8,0.0,0.0)], alpha=1.0, linewidths=0.6 )
plt.title( "Density Field" )
plt.yticks( (),() )
plt.xticks( (0,Box_L) )
plt.xlabel( "[$h^{-1}$ Mpc]" )


#Visual impression
plt.subplot( 1, 3, 2 )
Coor, X = CutHaloZ( Cut*Box_L/(1.0*N_sec)-dx/2.0, dx, GH, plot = False )
plt.plot( Coor[0], Coor[1], '.', color = 'blue', markersize = 1 )
#Visual impression of the density field base upon some cut offs
delta_visual = 0.0*(delta < -0.57) + 1.0*( -0.57 <= delta )*( delta< 0.60 ) \
+ 2.0*( 0.6 <= delta )*( delta < 8.82 ) + 3.0*( delta >= 8.82 )
plt.imshow( np.transpose(-delta_visual[::,::-1]), extent = extent, vmin=-3, vmax=0, cmap = my_cmap4 )
#plt.imshow( np.transpose(np.log( delta + 1 )[::,::-1]), extent = extent, cmap = "binary" )
plt.title( "Visual impresion" )
plt.yticks( (),() )
plt.xticks( (0,Box_L) )
plt.xlabel( "[$h^{-1}$ Mpc]" )


#Void Regions
plt.subplot( 1, 3, 3 )
#Voids basins
num_voids = np.max( voids )
lista = np.array([-1000] + list(np.random.permutation( range(1,num_voids.astype(int)+1) )))
#voids
voids = lista[ voids.astype(int) ]
plt.imshow( np.transpose(voids[::,::-1]), cmap = 'spectral', extent = extent, vmin = -num_voids/20., vmax = num_voids+1)
#interpolation='linear')
plt.title( "Distribution of voids" )
plt.yticks( (),() )
plt.xticks( (0,Box_L) )
plt.xlabel( "[$h^{-1}$ Mpc]" )

plt.xlim( (0,Box_L) )
plt.ylim( (0,Box_L) )



if sys.argv[2] == '1':
    if sys.argv[3] == 'png':
	plt.savefig( '%scosmicweb_density.png'%(figures_fold) )
    else:
	plt.savefig( '%scosmicweb_density.pdf'%(figures_fold) )
else:
    plt.show()