#halos_fraction.py
#
#This code calculates plots of fraction of halos in each one of the defined environments for a 
#range od threshold values
#Usage: halos_fraction.py <Vweb or Tweb> <BDM or FOF> <show(0) or save(1)>
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
#Colors
colors = [ 'green', 'blue', 'red', 'gray' ]

#==================================================================================================
#Fraction of halos in each environment
#==================================================================================================

plt.figure( figsize=(5,5) )

#Loading file of number fractions
numbers = np.loadtxt( '%shalos_count_regions_%s_%s.dat'%(data_figures_fold,catalogue,web) )
#Plotting 
plt.plot( numbers[:,0], numbers[:,1], linewidth = 2, label='voids', color = colors[0] )
plt.plot( numbers[:,0], numbers[:,2], linewidth = 2, label='sheets', color = colors[1] )
plt.plot( numbers[:,0], numbers[:,3], linewidth = 2, label='filaments', color = colors[2] )
plt.plot( numbers[:,0], numbers[:,4], linewidth = 2, label='knots', color = colors[3] )
plt.grid(1)
plt.ylabel( 'Fraction of halos', fontsize = 12 )
plt.xlabel( '$\lambda_{th}$', fontsize = 12 )
plt.xlim( (0,1) )
plt.ylim( (0,1) )
plt.title( '%s %s'%(web, catalogue) )
plt.legend( loc='upper left', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )
#Lambda_th line
if web == 'Tweb':
    lamb_opt = 0.36
elif web == 'Vweb':
    lamb_opt = 0.202
plt.vlines( lamb_opt, 0, 1, linestyle = '--', color = 'blue', linewidth = 2 )
plt.text( lamb_opt + 0.01, 0.6, '$\lambda_{opt}$', fontsize = 15, color='blue' )
#Show or save figure
if sys.argv[3] == '1':
    plt.savefig( '%shalos_fraction_%s_%s.pdf'%(figures_fold, catalogue, web) )
else:
    plt.show()