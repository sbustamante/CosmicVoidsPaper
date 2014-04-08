#cosmicweb_visual_impresion.py
#
#This code perform a graphic scheme of the visual impresion for a defined cutting off of Bolshoi
#simulation, using the density field and the two environment classification schemes
#
#by: Sebastian Bustamante

execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["BOLSHOI/"]
#Labels of graphs
labels = ["BOLSHOI"]
#Box lenght
Box_L = [250]
#Number of sections
N_sec = [256]
#Web scheme
web = 'Vweb'
#Values to evaluate lambda_th
#Lambda_ths = [ 0, 0.326/2.0, 0.326, 2*0.326 ]
Lambda_ths = [ 0, 0.188/2.0, 0.188, 2*0.188 ]
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
#			PLOTING EACH CLUES SIMULATION AND RESPECTIVE LG
#==================================================================================================
'''
FIGURE SCHEME
-------------------
|  1  |  2  |  3  |
-------------------
'''

N_sim = len( folds )
ax = np.zeros( (3, N_sim) )

i_fold = 0
plt.figure( figsize=(16,4*N_sim) )

for fold in folds:
    #Extent
    extent = [0, Box_L[i_fold], 0, Box_L[i_fold]]

    #Loading Density filename
    delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,fold,N_sec[i_fold],smooth)
    #Loading Vweb filename
    eig_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
    
    #Current label simulation
    label = labels[i_fold]
	
    #Loading Fields
    delta = CutFieldZ( delta_filename, Cut, 32, Coor = axe )
    eig1 = CutFieldZ( eig_filename+"_1", Cut, 16, Coor = axe )
    eig2 = CutFieldZ( eig_filename+"_2", Cut, 16, Coor = axe )
    eig3 = CutFieldZ( eig_filename+"_3", Cut, 16, Coor = axe )

    #Density Plot
    plt.subplot( N_sim, 5, 5*i_fold+1 )
    plt.imshow( np.log(1+delta), extent = extent, cmap = "binary" )
    if i_fold == 0: 
	plt.title( "Density\nField" )
    plt.ylabel( '%s'%(label) )
    plt.yticks( (0,Box_L[i_fold]) )
    plt.xticks( (0,Box_L[i_fold]) )
    #if i_fold == N_sim - 1:
	#plt.xlabel( "[$h^{-1}$ Mpc]" )
	
	
    #Vweb Plot with Lambda_th = 0
    plt.subplot( N_sim, 5, 5*i_fold+2 )
    lambda_th = Lambda_ths[0]
    plt.imshow( -Scheme( eig1, eig2, eig3, lambda_th ), extent = extent, vmin=-3, vmax=0, cmap = my_cmap4 )
    if i_fold == 0: 
	plt.title( "%s\n$\lambda_{th} = %1.3f$"%(web,lambda_th) )
    plt.yticks( (),() )
    plt.xticks( (0,Box_L[i_fold]) )
    #if i_fold == N_sim - 1:
	#plt.xlabel( "[$h^{-1}$ Mpc]" )
    
    
    #Vweb Plot with Lambda_th = 0.1
    plt.subplot( N_sim, 5, 5*i_fold+3 )
    lambda_th = Lambda_ths[1]
    plt.imshow( -Scheme( eig1, eig2, eig3, lambda_th ), extent = extent, vmin=-3, vmax=0, cmap = my_cmap4 )
    if i_fold == 0: 
	plt.title( "%s\n$\lambda_{th} = %1.3f$"%(web,lambda_th) )
    plt.yticks( (),() )
    plt.xticks( (0,Box_L[i_fold]) )
    if i_fold == N_sim - 1:
	plt.xlabel( "[$h^{-1}$ Mpc]" )
    
    
    #Vweb Plot with Lambda_th = 0.3
    plt.subplot( N_sim, 5, 5*i_fold+4 )
    lambda_th = Lambda_ths[2]
    plt.imshow( -Scheme( eig1, eig2, eig3, lambda_th ), extent = extent, vmin=-3, vmax=0, cmap = my_cmap4 )
    if i_fold == 0: 
	plt.title( "%s\n$\lambda_{th} = %1.3f$"%(web,lambda_th) )
    plt.yticks( (),() )
    plt.xticks( (0,Box_L[i_fold]) )
    #if i_fold == N_sim - 1:
	#plt.xlabel( "[$h^{-1}$ Mpc]" )
    
    
    #Vweb Plot with Lambda_th = 0.5
    plt.subplot( N_sim, 5, 5*i_fold+5 )
    lambda_th = Lambda_ths[3]
    plt.imshow( -Scheme( eig1, eig2, eig3, lambda_th ), extent = extent, vmin=-3, vmax=0, cmap = my_cmap4 )
    if i_fold == 0: 
	plt.title( "%s\n$\lambda_{th} = %1.3f$"%(web,lambda_th) )
    plt.yticks( (),() )
    plt.xticks( (0,Box_L[i_fold]) )
    #if i_fold == N_sim - 1:
	#plt.xlabel( "[$h^{-1}$ Mpc]" )
    

    plt.xlim( (0,Box_L[i_fold]) )
    plt.ylim( (0,Box_L[i_fold]) )

    i_fold += 1

#plt.subplots_adjust(  )
plt.show()