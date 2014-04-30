#cosmicweb_fractional_anisotropy.py
#
#This code perform a graphic scheme of the visual impresion for a defined cutting off of Bolshoi
#simulation, using the density field and FA is shown how is the behaviour of voids
#Usage cosmicweb_fractional_anisotropy.py <Vweb or Tweb> <show(0) or save(1)>
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
if web == 'Tweb':
    Lambda_opt = 0.36
if web == 'Vweb':
    Lambda_opt = 0.20
Lambda_opt = 0
#Smooth parameter
smooth = '_s1'
#Coordinate to cut (1 -- X, 2 -- Y, 3 -- Z)
axe = 1
#Cut
Cut = 10

#Colors
my_cmapC = plt.cm.get_cmap('gray')
my_cmap4 = plt.cm.get_cmap('gray', 4)

#==================================================================================================
#			PLOTING WEB SCHEME AND DENSITY FIELD FOR SIMULATION
#==================================================================================================
'''
FIGURE SCHEME
-------------------
|  1  |  2  |  3  |
-------------------
'''
plt.figure( figsize=(16,16) )
plt.subplots_adjust( top=0.93, bottom = 0.07, right = .98, left = 0.04, hspace = 0.14, wspace=0.0 )
#Extent
extent = [0, Box_L, 0, Box_L]

#Loading Density filename
delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,simulation,N_sec,smooth)
#Loading Vweb filename
eig_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,simulation,web,N_sec,smooth)

#Current label simulation
label = labels
    
#Loading Fields
delta = CutFieldZ( delta_filename, Cut, 32, Coor = axe )
eig1 = CutFieldZ( eig_filename+"_1", Cut, 16, Coor = axe )
eig2 = CutFieldZ( eig_filename+"_2", Cut, 16, Coor = axe )
eig3 = CutFieldZ( eig_filename+"_3", Cut, 16, Coor = axe )

#Vweb Plot with Lambda_th = 0.3
plt.subplot( 2, 2, 1 )
plt.imshow( -Scheme( eig1, eig2, eig3, Lambda_opt ), extent = extent, vmin=-3, vmax=0, cmap = my_cmap4 )
plt.title( "Vissual impresion for $\lambda_{th} = %1.3f$"%(Lambda_opt) )
plt.yticks( (),() )
plt.xticks( (0,Box_L) )
plt.xlabel( "[$h^{-1}$ Mpc]" )

#Vweb Plot with Lambda_th = 0
plt.subplot( 2, 2, 2 )
plt.imshow( Fractional_Anisotropy( eig1, eig2, eig3 ), extent = extent,  cmap = "binary" )
plt.title( "Fractional\nAnisotropy" )
plt.yticks( (),() )
plt.xticks( (0,Box_L) )
plt.xlabel( "[$h^{-1}$ Mpc]" )

#Vweb Plot with Lambda_th = 0.1
plt.subplot( 2, 2, 3 )
plt.contour( Fractional_Anisotropy( eig1, eig2, eig3 )[::-1,], 10, extent = extent )
plt.imshow( -Scheme( eig1, eig2, eig3, Lambda_opt ), extent = extent, vmin=-1, vmax=0, cmap = my_cmap4 )
plt.title( "FA for Voids at $\lambda_{th} = %1.3f$"%(Lambda_opt) )
plt.yticks( (),() )
plt.xticks( (0,Box_L) )
plt.xlabel( "[$h^{-1}$ Mpc]" )

#Density Plot
plt.subplot( 2, 2, 4 )
#plt.imshow( np.log10(1+delta), extent = extent, cmap = "binary" )
plt.contour( np.log(1+delta)[::-1,], np.linspace(np.min(np.log(1+delta)), 0,6), extent = extent )
plt.imshow( -Scheme( eig1, eig2, eig3, Lambda_opt ), extent = extent, vmin=-1, vmax=0, cmap = my_cmap4 )
plt.title( "Density for Voids at $\lambda_{th} = %1.3f$"%(Lambda_opt) )
plt.yticks( (0,Box_L) )
plt.xticks( (0,Box_L) )
plt.xlabel( "[$h^{-1}$ Mpc]" )


plt.xlim( (0,Box_L) )
plt.ylim( (0,Box_L) )

#plt.subplots_adjust(  )
if sys.argv[2] == '1':
    plt.savefig( '%scosmicweb_FA_%s(%1.2f).pdf'%(figures_fold, web,Lambda_opt ) )
else:
    plt.show()