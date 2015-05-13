#FA_delta_correlation.py
#
#This code plots the correlation between the fractional anisotropy and the density of each 
#web scheme
#Usage: FA_delta_correlation.py <show(0) or save(1)>
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
#Linestyles
linestyles = ["-", "--"]

#==================================================================================================
#Typical halo mass for each environment
#==================================================================================================
#Colors
plt.figure( figsize=(5.8,5) )

i_web = 0
for web in webs:
    #Loading files with quartiles
    quartiles = np.loadtxt( '%sFA_delta_%s.dat'%(data_figures_fold,web) )

    #Quartiles regions-------
    plt.fill_between( quartiles[:,0]+1, quartiles[:,1], quartiles[:,3], color = colors[i_web], alpha = 0.2 )
    plt.plot( quartiles[:,0]+1, quartiles[:,1], color = colors[i_web], linewidth = 1, linestyle = linestyles[i_web] )
    plt.plot( quartiles[:,0]+1, quartiles[:,3], color = colors[i_web], linewidth = 1, linestyle = linestyles[i_web] )

    #Medians-----------------
    plt.plot( quartiles[:,0]+1, quartiles[:,2], color = colors[i_web], linewidth = 3, label = web, \
    linestyle = linestyles[i_web] )
    
    plt.grid(1)
    plt.ylabel( 'FA', fontsize = 12 )
    plt.xlabel( '$\delta+1$', fontsize = 12)
    plt.xlim( (0.025,10) )
    plt.ylim( (0,1) )
    plt.legend( loc='lower right', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )
    
    i_web += 1

plt.semilogx( [0.0001,10], [0.95,0.95], '-', color='black', linewidth=2 )
plt.text( 0.03, 0.962, 'FA$_{th}$=0.95', fontsize = 12, color="black" )

if sys.argv[1] == '1':
    plt.savefig( '%sFA_delta.pdf'%(figures_fold) )
else:
    plt.show()