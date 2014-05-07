#halos_typical_velocity.py
#
#This code plots typical values (median and Q1 and Q3 quartiles) of dark matter peculiar velocity 
#in each type of environment according to Lambda_thr values
#Usage: halos_typical_mass.py <Vweb or Tweb> <BDM or FOF> <show(0) or save(1)>
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
web = sys.argv[1]
#Catalogue
catalogue = sys.argv[2]
#Colors and labels
colors = [ 'green', 'blue', 'red', 'black' ]
labels = [ 'voids', 'sheets', 'filaments', 'knots' ]

#==================================================================================================
#Typical halo peculiar velocity for each environment
#==================================================================================================
plt.figure( figsize=(5.8,5) )

#Loading files with quartiles
quartiles = np.loadtxt( '%shalos_velocities_%s_%s.dat'%(data_figures_fold,catalogue,web) )
quartiles[:,1:] = quartiles[:,1:]/1.0e2

#Quartiles regions-------
#Voids
plt.fill_between( quartiles[:,0], quartiles[:,1], quartiles[:,3], color = colors[0], alpha = 0.2 )
plt.plot( quartiles[:,0], quartiles[:,1], color = colors[0], linewidth = 1, linestyle = '--' )
plt.plot( quartiles[:,0], quartiles[:,3], color = colors[0], linewidth = 1, linestyle = '--' )
#Sheets
plt.fill_between( quartiles[:,0], quartiles[:,4], quartiles[:,6], color = colors[1], alpha = 0.2 )
plt.plot( quartiles[:,0], quartiles[:,4], color = colors[1], linewidth = 1, linestyle = '--' )
plt.plot( quartiles[:,0], quartiles[:,6], color = colors[1], linewidth = 1, linestyle = '--' )
#Filaments
plt.fill_between( quartiles[:,0], quartiles[:,7], quartiles[:,9], color = colors[2], alpha = 0.2 )
plt.plot( quartiles[:,0], quartiles[:,7], color = colors[2], linewidth = 1, linestyle = '--' )
plt.plot( quartiles[:,0], quartiles[:,9], color = colors[2], linewidth = 1, linestyle = '--' )
#Knots
plt.fill_between( quartiles[:,0], quartiles[:,10], quartiles[:,12], color = colors[3], alpha = 0.2 )
plt.plot( quartiles[:,0], quartiles[:,10], color = colors[3], linewidth = 1, linestyle = '--' )
plt.plot( quartiles[:,0], quartiles[:,12], color = colors[3], linewidth = 1, linestyle = '--' )

#Medians-----------------
#Voids
plt.plot( quartiles[:,0], quartiles[:,2], color = colors[0], linewidth = 3, label = "voids" )
#Filaments
plt.plot( quartiles[:,0], quartiles[:,8], color = colors[2], linewidth = 3, label = "filaments" )
#Sheets
plt.plot( quartiles[:,0], quartiles[:,5], color = colors[1], linewidth = 3, label = "sheets" )
#Knots
plt.plot( quartiles[:,0], quartiles[:,11], color = colors[3], linewidth = 3, label = "knots" )        

#Lambda_th line
#if web == 'Tweb':
    #lamb_opt = 0.36
#elif web == 'Vweb':
    #lamb_opt = 0.202
#plt.vlines( lamb_opt, 2, 12, linestyle = '--', color = 'blue', linewidth = 2 )
#plt.text( lamb_opt + 0.01, 7.6, '$\lambda_{opt}$=%1.2f'%(lamb_opt), fontsize = 12, color='blue' )

plt.grid(1)
plt.ylabel( '$|\\vec v_{pec}\ |$ $1\\times10^2$ km s$^{-1}$', fontsize = 12 )
plt.xlabel( '$\lambda_{th}$', fontsize = 12)
plt.xlim( (0,1) )
plt.ylim( (2,12) )
plt.legend( loc='upper right', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )
plt.title('%s %s'%(web, catalogue), fontweight="bold" )   

if sys.argv[3] == '1':
    plt.savefig( '%shalos_typical_velocity_%s_%s.pdf'%(figures_fold, catalogue, web) )
else:
    plt.show()