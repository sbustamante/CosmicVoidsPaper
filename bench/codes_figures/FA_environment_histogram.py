#FA_environment_histogram.py
#
#This code plots histograms for each environment according to different ranges of FA
#Usage: FA_environment_histogram.py <show(0) or save(1)>
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
colors = [ 'black', 'blue', 'red', 'green' ]
#Linestyles
linestyles = ["-", "--", "-.", ":"]
linewidths = [2,2,2,3]
#Labels
labels = ["voids", "sheets", "filaments", "knots"]

#==================================================================================================
#Typical halo mass for each environment
#==================================================================================================
#Colors
plt.figure( figsize=(5.8,5) )

i_web = 0
for web in webs:
    #Loading files with quartiles
    histogram = np.loadtxt( '%sFA_Environment_%s.dat'%(data_figures_fold,web) )

    for env in xrange(4):
	  plt.subplot(2,1,i_web+1)
	  hist, bins = np.histogram( histogram[:,0], bins = 50, weights = histogram[:,env+1], density=True )
	  if env == 0:
	      hist[bins[:-1]>0.95]=0
	  plt.plot( bins[:-1], hist, ls = linestyles[env], lw = linewidths[env],\
	  label = labels[env], color=colors[env] )
	
    i_web += 1

plt.subplot(2,1,1)
plt.legend( loc="upper left", fancybox=True, shadow=True, fontsize=12, ncol=2 )
plt.grid()
plt.xlim((0,1))
plt.ylim((0,25))
plt.ylabel("Probability Density $P(FA)$", fontsize = 11)
plt.text( 0.02, 6, "Tweb" )

plt.subplot(2,1,2)
plt.grid()
plt.xlim((0,1))
plt.ylim((0,25))
plt.xlabel("FA")
plt.ylabel("Probability Density $P(FA)$", fontsize = 11)
plt.text( 0.02, 6, "Vweb" )

if sys.argv[1] == '1':
    plt.savefig( '%sFA_environment.pdf'%(figures_fold) )
else:
    plt.show()