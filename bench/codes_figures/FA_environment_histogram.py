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

    hist = np.zeros( (50,4) )
    for env in xrange(4):
	  hist[:,env], bins = np.histogram( histogram[:,0], bins = 50, weights = histogram[:,env+1], density=True )
	  if env == 0:
	      hist[bins[:-1]>0.95,env]=0
    for env in xrange(4):
	  plt.subplot(2,1,i_web+1)
	  plt.plot( bins[:-1], hist[:,env]/(hist[:,0]+hist[:,1]+hist[:,2]+hist[:,3]), ls = linestyles[env], lw = linewidths[env],\
	  label = labels[env], color=colors[env] )
	
    i_web += 1

plt.subplot(2,1,1)
plt.legend( loc="center left", fancybox=True, shadow=True, fontsize=10, ncol=2 )
plt.grid()
plt.xlim((0,1))
plt.ylim((0,1))
plt.ylabel("$(dV_i/dFA)/(dV/dFA)$", fontsize = 11)
plt.text( 0.88, 0.9, "Tweb" )

plt.subplot(2,1,2)
plt.grid()
plt.xlim((0,1))
plt.ylim((0,1))
plt.xlabel("FA")
plt.ylabel("$(dV_i/dFA)/(dV/dFA)$", fontsize = 11)
plt.text( 0.88, 0.9, "Vweb" )

if sys.argv[1] == '1':
    plt.savefig( '%sFA_environment.pdf'%(figures_fold) )
else:
    plt.show()