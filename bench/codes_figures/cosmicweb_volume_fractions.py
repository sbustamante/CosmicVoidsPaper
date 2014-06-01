#cosmicweb_volume_fraction.py
#
#This code perform a graphic scheme of the visual impresion for a defined cutting off of Bolshoi
#simulation, using the FA, it is shown how is the behaviour of voids found through web schemes.
#Usage cosmicweb_fractional_anisotropy.py <Vweb or Tweb> <catalogue, BDM or FOF> <show(0) or save(1)>
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
    Lambda_opt = 0.265
if web == 'Vweb':
    Lambda_opt = 0.175
#Smooth parameter
smooth = '_s1'

#N Lambda
N_l = 100
#Lambdas Extremes
L_min = -0.3
L_max = 1
L_max += (L_max-L_min)/(1.0*N_l+1)

#==================================================================================================
#			PLOTING VOLUME FRACTION OF EACH REGION
#=================================================================================================='''
plt.figure( figsize=(5.8,5) )

#Loading Density filename
delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,simulation,N_sec,smooth)
#Loading Vweb filename
eig_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,simulation,web,N_sec,smooth)

#Making counts of each region
regs = Counts( eig_filename, delta_filename, L_min, L_max, N_l )

#Fraction of Voids
plt.fill_between( regs[0], regs[5]/regs[9], color = 'red' )
plt.plot( regs[0], regs[5]/regs[9], color = 'red', label = "voids", linewidth=2.0 )
#Fraction of Sheets
plt.fill_between( regs[0], (regs[5]+regs[6])/regs[9], regs[5]/regs[9], color = 'blue' )
plt.plot( regs[0], (regs[5]+regs[6])/regs[9], color = 'blue', label = "sheets", linewidth=2.0 )
#Fraction of Filaments
plt.fill_between( regs[0], (regs[5]+regs[6]+regs[7])/regs[9], (regs[5]+regs[6])/regs[9], color = 'green' )
plt.plot( regs[0], (regs[5]+regs[6]+regs[7])/regs[9], color = 'green', label = "filaments", linewidth=2.0 )
#Fraction of Knots
plt.fill_between( regs[0], 1.0, (regs[5]+regs[6]+regs[7])/regs[9], color = 'gray' )
plt.plot( regs[0], regs[0]*0.0, color = 'gray', label = "knots", linewidth=2.0 )

plt.xlim( L_min, 1.0 )
plt.legend( loc='lower right', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )
plt.xlabel( "$\lambda_{th}$" )
plt.ylabel( "Volume fraction" )
#Lambda_th line

plt.text( Lambda_opt + 0.03, 0.3, '$\lambda^%s_{opt}$=%1.3f'%(web[0],Lambda_opt), fontsize = 12,\
color = "black", rotation = 90 )
plt.plot( [Lambda_opt,Lambda_opt], [0, 1.0], linestyle = '-', color = "black", linewidth = 2 )

#plt.subplots_adjust(  )
if sys.argv[2] == '1':
    plt.savefig( '%scosmicweb_volume_%s.pdf'%(figures_fold, web ) )
else:
    plt.show()