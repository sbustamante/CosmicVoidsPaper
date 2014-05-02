#central_voids.py
#
#This code plots different properties of the central cells of voids, such as lambda_1 value, FA and
#finally density
#Usage: central_voids.py <show(0) or save(1)>
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
#Web Scheme
webs = ['Tweb', 'Vweb']
#Colors and labels
colors = [ 'red', 'blue' ]
#Number of neighbour cells
b = [1,2]
#Bins
bins = [100, 50, 50]

#==================================================================================================
#Typical halo mass for each environment
#==================================================================================================
#Colors
plt.figure( figsize=(15,5) )
plt.subplots_adjust( right = 0.99, left = 0.03 )

i_web = 0
for web in webs:
    #Loading files with quartiles
    properties1 = np.loadtxt( '%scentral_void_cells_%s_b%d.dat'%(data_figures_fold,web,b[0]) )
    properties2 = np.loadtxt( '%scentral_void_cells_%s_b%d.dat'%(data_figures_fold,web,b[1]) )
    
    #Lambda_1 eigenvalue
    plt.subplot(1,3,1)
    #Making histogram
    hist1d = np.histogram( properties1[:,3] , bins=bins[0], normed=True )
    hist1d2 = np.histogram( properties2[:,3] , bins=bins[0], normed=True )
    #Plotting
    plt.plot(hist1d[1][:-1], hist1d[0], color = colors[i_web], linewidth = 3, label = "%s"%(web))
    plt.plot(hist1d2[1][:-1], hist1d2[0], color = colors[i_web], linewidth = 1, linestyle = "-")
    plt.grid(1)
    plt.ylabel( 'Normed distribution', fontsize = 12 )
    plt.xlabel( '$\lambda_{1}$', fontsize = 12)
    plt.legend( loc='upper right', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )    
    plt.xlim( (-0.3,1.5) )
    
    #FA eigenvalue
    plt.subplot(1,3,2)
    #Making histogram
    hist1d = np.histogram( properties1[:,4] , bins=bins[1], normed=True )
    hist1d2 = np.histogram( properties2[:,4] , bins=bins[1], normed=True )
    #Plotting
    plt.plot(hist1d[1][:-1], hist1d[0], color = colors[i_web], linewidth = 3, label = "%s"%(web))
    plt.plot(hist1d2[1][:-1], hist1d2[0], color = colors[i_web], linewidth = 1, linestyle = "-")
    plt.grid(1)
    plt.ylabel( 'Normed distribution', fontsize = 12 )
    plt.xlabel( 'FA', fontsize = 12)
    plt.legend( loc='upper right', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )    
        
    #FA eigenvalue
    plt.subplot(1,3,3)
    #Making histogram
    hist1d = np.histogram( properties1[:,5] , bins=bins[2], normed=True )
    hist1d2 = np.histogram( properties2[:,5] , bins=bins[2], normed=True )
    #Plotting
    plt.plot(hist1d[1][:-1], hist1d[0], color = colors[i_web], linewidth = 3, label = "%s"%(web))
    plt.plot(hist1d2[1][:-1], hist1d2[0], color = colors[i_web], linewidth = 1, linestyle = "-")
    plt.grid(1)
    plt.ylabel( 'Normed distribution', fontsize = 12 )
    plt.xlabel( 'Density contrast $\delta$', fontsize = 12)
    plt.legend( loc='upper right', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )    
        
    i_web += 1
   

if sys.argv[1] == '1':
    plt.savefig( '%scentral_voids.pdf'%(figures_fold) )
else:
    plt.show()