#delta_L1_correlation.py
#
#This code plots the correlation between the density and the eigenvalue L1 of each web scheme
#Usage: FA_L1_correlation.py <show(0) or save(1)>
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

#==================================================================================================
#Typical halo mass for each environment
#==================================================================================================
#Colors
plt.figure( figsize=(5.8,5) )

i_web = 0
for web in webs:
    #Loading files with quartiles
    quartiles = np.loadtxt( '%sdelta_L1_%s.dat'%(data_figures_fold,web) )
    
    #Quartiles regions-------
    plt.fill_between( quartiles[:,0], quartiles[:,1], quartiles[:,3], color = colors[i_web], alpha = 0.2 )
    plt.plot( quartiles[:,0], quartiles[:,1], color = colors[i_web], linewidth = 1, linestyle = '--' )
    plt.plot( quartiles[:,0], quartiles[:,3], color = colors[i_web], linewidth = 1, linestyle = '--' )

    #Medians-----------------
    plt.plot( quartiles[:,0], quartiles[:,2], color = colors[i_web], linewidth = 3, label = web )

    plt.grid(1)
    plt.ylabel( '$\\rho$', fontsize = 12 )
    plt.xlabel( '$\lambda_{1}$', fontsize = 12)
    plt.xlim( (-0.2,2) )
    plt.ylim( (-1,0.5) )
    plt.legend( loc='lower right', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )
    #Lambda_th line
    if web == 'Tweb':
	lamb_opt = 0.36
    elif web == 'Vweb':
	lamb_opt = 0.202
    plt.vlines( lamb_opt, -1, 0.5, linestyle = '-', color = colors[i_web], linewidth = 2 )
    plt.text( lamb_opt + 0.02, 0.3, '$\lambda^%s_{opt}$=%1.2f'%(web[0],lamb_opt), fontsize = 12,\
    color=colors[i_web], rotation=90 )
    
    i_web += 1

if sys.argv[1] == '1':
    plt.savefig( '%sdelta_L1.pdf'%(figures_fold) )
else:
    plt.show()