#void_percolation_analysis.py
#
#This code calculate an percolation analysis of the three void finder schemes with respecto to the
#nth-order median filtering
#Usage void_percolation_analysis.py <show(0) or save(1)>
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
#Web Scheme
webs = ['Tweb', 'Vweb', 'Tweb'] 
labels = ['FA-Tweb', 'FA-Vweb', 'Density']
#Void finder schemes
void_schemes = ['FAG','FAG','DLG']
#Order of median filtering
Nfilter = 15
#Minim volum to consider a void
VOL = 0

#Colors
colors = ["green", "blue", "red"]

#==================================================================================================
#			CONSTRUCTING FIGURE
#==================================================================================================

i_web = 0
for web in webs:
    print simulation, web
    
    VoidsNumber0 = []
    VoidsVolume0 = []
    VoidsMedian0 = []
    VoidsNumber1 = []
    VoidsVolume1 = []
    VoidsMedian1 = []
    
    for iter in arange(0,Nfilter+1):
	#Loading external void catalogue without boundary removals
	void_regs = np.transpose(np.loadtxt("%s/%s/%s/%d/voids%s/voids_%d0/void_regions.dat"%\
	(foldglobal, simulation, web, N_sec, void_schemes[i_web], iter )))
      
	VoidsNumber0.append( (void_regs[0,void_regs[1,:]>VOL])[-1] )
	VoidsVolume0.append( void_regs[1,void_regs[1,:]>VOL][0] )
	VoidsMedian0.append( np.mean(void_regs[1,void_regs[1,:]>VOL]) )
	
	#Loading external void catalogue with boundary removals
	void_regs = np.transpose(np.loadtxt("%s/%s/%s/%d/voids%s/voids_%d1/void_regions.dat"%\
	(foldglobal, simulation, web, N_sec, void_schemes[i_web], iter )))
      
	VoidsNumber1.append( (void_regs[0,void_regs[1,:]>VOL])[-1] )
	VoidsVolume1.append( void_regs[1,void_regs[1,:]>VOL][0] )
	VoidsMedian1.append( np.mean(void_regs[1,void_regs[1,:]>VOL]) )
	
    VoidsNumber0 = np.array( VoidsNumber0 )
    VoidsVolume0 = np.array( VoidsVolume0 )
    VoidsMedian0 = np.array( VoidsMedian0 )
    
    VoidsNumber1 = np.array( VoidsNumber1 )
    VoidsVolume1 = np.array( VoidsVolume1 )
    VoidsMedian1 = np.array( VoidsMedian1 )
	
    plt.subplot(121)
    plt.plot( VoidsNumber0/10000., color = colors[i_web], linestyle = "--", linewidth = 2 )
    plt.plot( VoidsNumber1/10000., color = colors[i_web], linestyle = "-", linewidth = 2 )
    
    plt.subplot(122)
    plt.plot( VoidsVolume0/10000., color = colors[i_web], linestyle = "--", linewidth = 2 )
    plt.plot( VoidsVolume1/10000., color = colors[i_web], linestyle = "-", linewidth = 2, label = labels[i_web] )
    
    #plt.plot( VoidsMedian0/10000., color = colors[i_web], linestyle = "--", linewidth = 2 )
    #plt.plot( VoidsMedian1/10000., color = colors[i_web], linestyle = "-", linewidth = 2, label = labels[i_web] )
	
    i_web += 1
    
    
#Formating figures
plt.subplot(121)
plt.grid()

plt.subplot(122)
plt.legend( loc='upper left', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )
plt.grid()


if sys.argv[1] == '1':
    plt.savefig( '%svoids_percolation_analysis.pdf'%(figures_fold) )
else:
    plt.show()