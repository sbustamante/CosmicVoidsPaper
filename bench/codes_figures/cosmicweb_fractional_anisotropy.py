
#cosmicweb_fractional_anisotropy.py
#
#This code perform a graphic scheme of the visual impresion for a defined cutting off of Bolshoi
#simulation, using the FA, it is shown how is the behaviour of voids found through web schemes.
#Usage cosmicweb_fractional_anisotropy.py <Vweb or Tweb> <catalogue, BDM or FOF> <order MF and BR>
#					  <show(0) or save(1)> <format (png, pdf)>
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
#Void parameters ( Nth-order median filtering,  Boolean for boundary removals )
config = sys.argv[3]

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
cmap2 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap2',["white","black"],2)
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
#Loading Mass filename
mass_filename = '%s%sVweb/%d/M'%(foldglobal,simulation,N_sec)
#Loading Momentums filename
px_filename = '%s%sVweb/%d/P_0'%(foldglobal,simulation,N_sec)
py_filename = '%s%sVweb/%d/P_1'%(foldglobal,simulation,N_sec)
pz_filename = '%s%sVweb/%d/P_2'%(foldglobal,simulation,N_sec)
#Loading Vweb filename
eig_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,simulation,web,N_sec,smooth)
#Loading general catalog of halos
GH = np.loadtxt('%s%sC_GH_%s.dat'%(foldglobal,simulation,catalog))
#Catalogue of voids
voids = CutFieldZ( "%s/%s/%s/%d/voids%s/voids_%s/void_index.dat"%\
(foldglobal, simulation, web, N_sec, void_scheme, config ), Cut, 'plain', Coor = axe )

#Loading Fields
delta = CutFieldZ( delta_filename, Cut, 32, Coor = axe )
eig1 = CutFieldZ( eig_filename+"_1", Cut, 16, Coor = axe )
eig2 = CutFieldZ( eig_filename+"_2", Cut, 16, Coor = axe )
eig3 = CutFieldZ( eig_filename+"_3", Cut, 16, Coor = axe )
mass = CutFieldZ( mass_filename, Cut, 32, Coor = axe )
px = CutFieldZ( px_filename, Cut, 32, Coor = axe )
py = CutFieldZ( py_filename, Cut, 32, Coor = axe )
pz = CutFieldZ( pz_filename, Cut, 32, Coor = axe )

#Calculating contour of voids
contours = np.zeros( (N_sec,N_sec) )
#Sweeping matrix
for i in xrange(N_sec):
    for j in xrange(N_sec):
	for ic in arange(-1,2):
	    for jc in arange(-1,2):
		#Indexes of neighbours
		it = i + ic
		jt = j + jc
		if i + ic >= N_sec: it = 0
		if i + ic < 0: it = N_sec-1
		if j + jc >= N_sec: jt = 0
		if j + jc < 0: jt = N_sec-1
		#Marking contours
		if( voids[i,j] != voids[it,jt] ):
		    contours[i,j] = 1

#FA field
plt.subplot( 1, 3, 1 )
plt.imshow( np.transpose(Fractional_Anisotropy( eig1, eig2, eig3 )[::,::-1]), extent = extent, cmap = "hot_r" )
#plt.contour( np.transpose(Fractional_Anisotropy( eig1, eig2, eig3 )), levels=[0.95], extent = extent, \
#colors="red", alpha=0.5, linewidths=0.6 )
#plt.imshow( Scheme( eig1, eig2, eig3, 0.0 )[::-1,], extent = extent, vmin=0, vmax=0.5, cmap = cmap2, origin='lower' )
plt.title( "Fractional Anisotropy (%s)"%web )
plt.yticks( (),() )
plt.xticks( (0,Box_L) )
plt.xlabel( "[$h^{-1}$ Mpc]" )

plt.colorbar( orientation = "horizontal", fraction = 0.05, pad = 0.02 )

##Visual impression
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
extent = [0, N_sec, 0, N_sec]
#Coor, X = CutHaloZ( Cut*Box_L/(1.0*N_sec)-dx/2.0, dx, GH, plot = False )
#plt.plot( Coor[0], Coor[1], 'o', color = 'white', markersize = 4 )
#Void basins
num_voids = np.max( voids )
lista = np.array([nan] + list(np.random.permutation( range(1,num_voids.astype(int)+1) )))
#voids
voids2 = lista[ voids.astype(int) ]
plt.imshow( np.transpose(voids2[::,::-1]), cmap = 'spectral', extent = extent, vmin = -num_voids/20., vmax = num_voids,\
interpolation = 'none' )
plt.imshow( np.transpose(contours[::,::-1]), cmap = cmap2, extent = extent, vmin = 0, vmax = 1 )

#Velocity field
X,Y = meshgrid( arange(0,N_sec,1),arange(0,N_sec,1) )
Vx = np.transpose((np.sign(px)*np.abs(px)/(1.0*mass))[::,::-1])
Vy = np.transpose((np.sign(py)*np.abs(py)/(1.0*mass))[::,::])
norm = 100.
#quiver( X, Y, Vx/norm, Vy/norm, color='k', units='x', zorder=2, scale = 1, alpha=0.2)

plt.title( "Distribution of voids" )
plt.yticks( (),() )
plt.xticks( (0,Box_L) )
plt.xlabel( "[$h^{-1}$ Mpc]" )

plt.xlim( (0,Box_L) )
plt.ylim( (0,Box_L) )


if sys.argv[4] == '1':
    if sys.argv[5] == 'png':
	plt.savefig( '%scosmicweb_FA_%s.png'%(figures_fold, web ) )
    else:
	plt.savefig( '%scosmicweb_FA_%s.pdf'%(figures_fold, web ) )
else:
    plt.show()