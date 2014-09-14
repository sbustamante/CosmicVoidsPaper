#FA_Prolatenes_MonteCarlo.py
#
#This code performs an study of the FA and the Prolatenes index through a montecarlo generation of
#spheroidal distributions.
#Usage FA_Prolatenes_MonteCarlo.py <0-FA-Prol distro    1-Spheroids_Picture >
#
#by: Sebastian Bustamante

execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Number of points
N = 50000
#Normalization condition
Rmax = 3.0
Rmin = -1.0
#Scale of the plot
Nscale = 1.0
#Number of intervals
n_fa = int(10/Nscale)+1
n_p = int(10/Nscale)
#Tiny value of the FA and the prolatenes (<0.5)
frac = 0.47

#==================================================================================================
#			FUNCTIONS
#==================================================================================================
#Fractional Anisotropy
def FA( l1, l2, l3 ):
    return np.sqrt( ( (l1-l3)**2 + (l2-l3)**2 + (l1-l2)**2 )/(3*(l1**2+l2**2+l3**2)) )
  
#Prolatenes
def P(l1,l2,l3):
    #return ( l3+l1-2*l2 )/( l3-l1 )   		#Non normalized
    #return ( l3+l1-2*l2 )/abs( 2*(l1+l2+l3) )	#Classical normalization
    return -( l3+l1-2*l2 )/(l1**2+l2**2+l3**2)	#My normalization

#==================================================================================================
#			GENERATION
#==================================================================================================
fa = []
p = []
l = []
for i in xrange(N):
    xi = Rmin + (Rmax-Rmin)*np.random.random()
    yi = Rmin + (Rmax-Rmin)*np.random.random()
    zi = Rmin + (Rmax-Rmin)*np.random.random()
    ls = np.sort( [xi, yi, zi] )/norm([xi, yi, zi])
    l.append(ls)
    #Prolatenes
    p.append( P( ls[0], ls[1], ls[2] ) )
    #Fractional Anisotropy
    fa.append( FA( ls[0], ls[1], ls[2] ) )
    
p = np.array(p)
fa = np.array(fa)
l = np.array(l)
    
    
#==================================================================================================
#			SCATTER PLOT
#==================================================================================================
if sys.argv[1] == "0":
    plt.plot( p, fa, '.' )
    plt.xlim( (-2,2) )
    plt.show()
    
    
#==================================================================================================
#			DISTRIBUTION PLOT 
#==================================================================================================
if sys.argv[1] == "1":
    fa_array = np.linspace(0,1,n_fa);
    p_array = np.linspace(-1.3,1.3,n_p)
    fa_tin = 1.0/(n_fa-1)*frac
    p_tin = 1.0/(n_p-1)*frac

    for fai in xrange(n_fa-1):
	for pi in xrange(n_p-1):
	    fig = plt.figure(figsize=(6,6))  # Square figure
	    fig.subplots_adjust( top = 1.0, right = 1.0, bottom = 0.0, left = 0.0 )
	    ax = fig.add_subplot(111, projection='3d')

	    try:
		coef = l[ (fa<fa_array[fai+1]-fa_tin)*(fa>=fa_array[fai]+fa_tin)*(p<p_array[pi+1]-p_tin)*(p>=p_array[pi]+p_tin) ][0]
		coef = coef - Rmin
		
		rx, ry, rz = 1.0/coef

		# Set of all spherical angles:
		u = np.linspace(0, 2 * np.pi, 100)
		v = np.linspace(0, np.pi, 100)

		# Cartesian coordinates that correspond to the spherical angles:
		# (this is the equation of an ellipsoid):
		x = rx * np.outer(np.cos(u), np.sin(v))
		y = ry * np.outer(np.sin(u), np.sin(v))
		z = rz * np.outer(np.ones_like(u), np.cos(v))

		# Plot:
		ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b')

		# Adjustment of the axes, so that they all have the same span:
		max_radius = max(rx, ry, rz)*2/3.
		for axis in 'xyz':
		    getattr(ax, 'set_{}lim'.format(axis))((-max_radius, max_radius))
	    except:
		None
	
	    plt.axis('off')
	    plt.savefig( "tmp_%d%d.png"%(fai,pi), dpi=10*Nscale )
	    plt.close()
	    

    #Creating final plot---------------------------------------------------------------------------
    fig = plt.figure( figsize=(7,7) )
    ax = fig.add_subplot(111)

    for fai in xrange(n_fa-1):
	for pi in xrange(n_p-1):
	    im = Image.open("./tmp_%d%d.png"%(fai,pi) )
	    height = im.size[1]
	    fig.figimage(im, 75+30*Nscale+Nscale*60*pi, 55+60*Nscale*fai, zorder = 2)
	    
	    ax.set_xlim( -1.2, 1.2 )
	    ax.set_ylim( 0, 1 )
	    fig.subplots_adjust( top = 0.96, right = 0.99, bottom = 0.06, left = 0.08 )
	    ax.set_xlabel( "Prolatenes" )
	    ax.set_ylabel( "Fractional Anisotropy" )
	    
    fig.savefig( '%sFA_Prolatenes.png'%(figures_fold) )
    
    os.system( "rm *.png" )