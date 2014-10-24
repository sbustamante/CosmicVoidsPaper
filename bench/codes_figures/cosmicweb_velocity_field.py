#cosmicweb_velocity_field.py
#
#This code sketches and slide of the simulation, showing the density field along with the velocity
#field projected
#cosmicweb_velocity_field.py <show(0) or save(1)> <format (png, pdf)>
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

#Smooth parameter
smooth = '_s1'
#Coordinate to cut (1 -- X, 2 -- Y, 3 -- Z)
axe = 1
#Cut
Cut = 50
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
plt.figure( figsize=(8,8) )
#Extent
extent = [0, N_sec, 0, N_sec]

#Loading Density filename
delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,simulation,N_sec,smooth)
#Loading Mass filename
mass_filename = '%s%sVweb/%d/M'%(foldglobal,simulation,N_sec)
#Loading Momentums filename
px_filename = '%s%sVweb/%d/P_0'%(foldglobal,simulation,N_sec)
py_filename = '%s%sVweb/%d/P_1'%(foldglobal,simulation,N_sec)
pz_filename = '%s%sVweb/%d/P_2'%(foldglobal,simulation,N_sec)

#Loading Fields
delta = CutFieldZ( delta_filename, Cut, 32, Coor = axe )
mass = CutFieldZ( mass_filename, Cut, 32, Coor = axe )
px = CutFieldZ( px_filename, Cut, 32, Coor = axe )
py = CutFieldZ( py_filename, Cut, 32, Coor = axe )
pz = CutFieldZ( pz_filename, Cut, 32, Coor = axe )

#plt.imshow( np.transpose(np.log( delta + 1 )[::,::-1]), extent = extent, cmap = "hot", alpha=0.5 )

X,Y = meshgrid( arange(0,N_sec,1),arange(0,N_sec,1) )
Vx = np.transpose((np.sign(px)*np.abs(px)/(1.0*mass))[::,::-1])
#Vx = np.transpose((px/(1.0*mass))[::,::-1])
Vy = np.transpose((np.sign(py)*np.abs(py)/(1.0*mass))[::,::])
#Vz = np.transpose((np.sign(pz)*np.abs(pz)/(1.0*mass))[::,::-1])

norm = 100.#np.sqrt( Vx**2 + Vy**2 )
quiver( X, Y, Vx/norm, Vy/norm, color='k', units='x', zorder=2, scale = 1, alpha=0.2)#headaxislength=5)
plt.imshow( np.transpose(np.log( delta + 1 )[::,::-1]), extent = extent, cmap = "hot", alpha=0.99 )
plt.xlim((0,N_sec))
plt.ylim((0,N_sec))
#plt.contour( np.transpose(delta), levels=[-0.57], extent = extent, linestyles="-",\
#colors=[(0.8,0.0,0.0)], alpha=1.0, linewidths=0.6 )

plt.title( "Density Field" )
plt.yticks( (),() )
plt.xticks( (0,Box_L) )
plt.xlabel( "[$h^{-1}$ Mpc]" )

if sys.argv[1] == '1':
    if sys.argv[2] == 'png':
	plt.savefig( '%scosmicweb_density.png'%(figures_fold) )
    else:
	plt.savefig( '%scosmicweb_density.pdf'%(figures_fold) )
else:
    plt.show()