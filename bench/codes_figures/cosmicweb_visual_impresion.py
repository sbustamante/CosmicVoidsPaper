#cosmicweb_visual_impresion.py
#
#This code perform a graphic scheme of the visual impresion for a defined cutting off of Bolshoi
#simulation, using the density field and the two environment classification schemes
#Usage cosmicweb_visual_impresion.py <Vweb or Tweb> <show(0) or save(1)>
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
Lambda_ths = [ 0, Lambda_opt/2.0, Lambda_opt, 2*Lambda_opt ]
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
plt.figure( figsize=(16,4) )

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

#Density Plot
plt.subplot( 1, 5, 1 )
plt.imshow( np.log(1+delta), extent = extent, cmap = "binary" )
plt.title( "Density\nField" )
plt.ylabel( '%s'%(label) )
plt.yticks( (0,Box_L) )
plt.xticks( (0,Box_L) )
        
#Vweb Plot with Lambda_th = 0
plt.subplot( 1, 5, 2 )
lambda_th = Lambda_ths[0]
plt.imshow( -Scheme( eig1, eig2, eig3, lambda_th ), extent = extent, vmin=-3, vmax=0, cmap = my_cmap4 )
plt.title( "%s\n$\lambda_{th} = %1.3f$"%(web,lambda_th) )
plt.yticks( (),() )
plt.xticks( (0,Box_L) )

#Vweb Plot with Lambda_th = 0.1
plt.subplot( 1, 5, 3 )
lambda_th = Lambda_ths[1]
plt.imshow( -Scheme( eig1, eig2, eig3, lambda_th ), extent = extent, vmin=-3, vmax=0, cmap = my_cmap4 )
plt.title( "%s\n$\lambda_{th} = %1.3f$"%(web,lambda_th) )
plt.yticks( (),() )
plt.xticks( (0,Box_L) )
plt.xlabel( "[$h^{-1}$ Mpc]" )

#Vweb Plot with Lambda_th = 0.3
plt.subplot( 1, 5, 4 )
lambda_th = Lambda_ths[2]
plt.imshow( -Scheme( eig1, eig2, eig3, lambda_th ), extent = extent, vmin=-3, vmax=0, cmap = my_cmap4 )
plt.title( "%s\n$\lambda_{th} = %1.3f$"%(web,lambda_th) )
plt.yticks( (),() )
plt.xticks( (0,Box_L) )

#Vweb Plot with Lambda_th = 0.5
plt.subplot( 1, 5, 5 )
lambda_th = Lambda_ths[3]
plt.imshow( -Scheme( eig1, eig2, eig3, lambda_th ), extent = extent, vmin=-3, vmax=0, cmap = my_cmap4 )
plt.title( "%s\n$\lambda_{th} = %1.3f$"%(web,lambda_th) )
plt.yticks( (),() )
plt.xticks( (0,Box_L) )

plt.xlim( (0,Box_L) )
plt.ylim( (0,Box_L) )

#plt.subplots_adjust(  )
if sys.argv[2] == '1':
    plt.savefig( '%scosmicweb_visual_%s.pdf'%(figures_fold, web) )
else:
    plt.show()