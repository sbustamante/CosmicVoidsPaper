
#cosmicweb_fractional_anisotropy.py
#
#This code perform a graphic scheme of the visual impresion for a defined cutting off of Bolshoi
#simulation, using the FA, it is shown how is the behaviour of voids found through web schemes.
#Usage cosmicweb_fractional_anisotropy.py <Vweb or Tweb> <catalogue, BDM or FOF> <show(0) or save(1)>
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

#Web scheme
web = sys.argv[1]

#Halo Scheme
catalog = sys.argv[2]

#Void catalogue
void_scheme = "FAG"
#Void parameter (For FAG scheme, it corresponds to the number of iterations for the median filtering)
lambda_void = 0.0

#Values to evaluate lambda_th
if web == 'Tweb':
    Lambda_opt = 0.265
if web == 'Vweb':
    Lambda_opt = 0.175
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
#Loading Vweb filename
eig_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,simulation,web,N_sec,smooth)
#Loading general catalog of halos
GH = np.loadtxt('%s%sC_GH_%s.dat'%(foldglobal,simulation,catalog))
#Catalogueof voids
voids = CutFieldZ( "%s/%s/%s/%d/voids%s/voids_%1.2f/void_index.dat"%\
(foldglobal, simulation, web, N_sec, void_scheme, lambda_void ), Cut, 'plain', Coor = axe )    
#Loading Fields
delta = CutFieldZ( delta_filename, Cut, 32, Coor = axe )
eig1 = CutFieldZ( eig_filename+"_1", Cut, 16, Coor = axe )
eig2 = CutFieldZ( eig_filename+"_2", Cut, 16, Coor = axe )
eig3 = CutFieldZ( eig_filename+"_3", Cut, 16, Coor = axe )


#FA field
plt.subplot( 1, 3, 1 )
plt.imshow( np.transpose(Fractional_Anisotropy( eig1, eig2, eig3 )[::,::-1]), extent = extent, cmap = "binary" )
plt.contour( np.transpose(Fractional_Anisotropy( eig1, eig2, eig3 )), levels=[0.95], extent = extent, \
colors="red", alpha=0.5, linewidths=0.6 )
#plt.imshow( Scheme( eig1, eig2, eig3, 0.0 )[::-1,], extent = extent, vmin=0, vmax=0.5, cmap = cmap2, origin='lower' )
plt.title( "Fractional Anisotropy (%s)"%web )
plt.yticks( (),() )
plt.xticks( (0,Box_L) )
plt.xlabel( "[$h^{-1}$ Mpc]" )


#Visual impression
plt.subplot( 1, 3, 2 )
Coor, X = CutHaloZ( Cut*Box_L/(1.0*N_sec)-dx/2.0, dx, GH, plot = False )
plt.plot( Coor[0], Coor[1], '.', color = 'blue', markersize = 1 )
plt.imshow( -np.transpose(Scheme( eig1, eig2, eig3, Lambda_opt )[::,::-1]), extent = extent, vmin=-3, vmax=0, cmap = my_cmap4 )
plt.title( "Visual impresion for $\lambda_{th} = %1.3f$"%(Lambda_opt) )
plt.yticks( (),() )
plt.xticks( (0,Box_L) )
plt.xlabel( "[$h^{-1}$ Mpc]" )


#Void Regions
plt.subplot( 1, 3, 3 )
#Coor, X = CutHaloZ( Cut*Box_L/(1.0*N_sec)-dx/2.0, dx, GH, plot = False )
#plt.plot( Coor[0], Coor[1], 'o', color = 'white', markersize = 4 )
#Voids basins
num_voids = np.max( voids )
lista = np.array([-1000] + list(np.random.permutation( range(1,num_voids.astype(int)+1) )))
#voids
voids = lista[ voids.astype(int) ]
plt.imshow( np.transpose(voids[::,::-1]), cmap = 'spectral', extent = extent, vmin = -1000, vmax = num_voids+1)
#interpolation='linear')
plt.title( "Distribution of voids" )
plt.yticks( (),() )
plt.xticks( (0,Box_L) )
plt.xlabel( "[$h^{-1}$ Mpc]" )

plt.xlim( (0,Box_L) )
plt.ylim( (0,Box_L) )


##Void Regions
#plt.subplot( 1, 4, 4 )
##Distribution of halos
#Coor, X = CutHaloZ( Cut*Box_L/(1.0*N_sec)-dx/2.0, dx, GH, plot = False )
#plt.plot( Coor[0], Coor[1], 'o', color = 'black', markersize = 2 )
#plt.imshow( np.transpose(voids[::,::-1]), cmap = 'spectral', interpolation='none', extent = extent,
#vmin = 0, vmax = num_voids+1, alpha=0.0)
#plt.title( "Distribution of halos" )
#plt.yticks( (),() )
#plt.xticks( (0,Box_L) )
#plt.xlabel( "[$h^{-1}$ Mpc]" )

#plt.xlim( (0,Box_L) )
#plt.ylim( (0,Box_L) )

#plt.subplots_adjust(  )
if sys.argv[3] == '1':
    plt.savefig( '%scosmicweb_FA_%s.pdf'%(figures_fold, web ) )
else:
    plt.show()