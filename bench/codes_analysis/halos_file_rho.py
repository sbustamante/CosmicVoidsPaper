#halos_file_rho.py
#
#This code builds a data file with tabulated densities corresponding to each halo, both BDM and
#FOF schemes.
#
#Usage: run halos_file_lambdas.py <Vweb or Tweb> <BDM or FOF>
#
#by: Sebastian Bustamante

execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
simulation = "BOLSHOI/"
#Box lenght
Box_L = 250
#Number of sections
N_sec = 256
#Smooth parameter
smooth = '_s1'
#Web Scheme
web = sys.argv[1]
#Catalog Scheme
catalog = sys.argv[2]

#==================================================================================================
#			CONSTRUCTING FILES WITH HALOS ENVIRONMENT
#==================================================================================================
    
#Box Lenght
L = Box_L

#Loading Eigenvalues Vweb filename
eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec,smooth)
#Loading All properties of Halos
halos = np.transpose(np.loadtxt('%s%s/C_GH_%s.dat'%(foldglobal,fold, catalog)))
datos = np.transpose(np.loadtxt('%s%s/C_GH_%s.dat'%(foldglobal,fold, catalog)))
Nhalos = len(halos[0])

#Saving environment of each halo
eig = np.zeros( (3,Nhalos) )
for i in xrange( N_sec ):
    #Showing the advance
    progress(50, int(100*i/(1.0*N_sec)) )
    
    #loading index of halos in a same X cut
    temp, index = CutHaloX( 
    i*L*1.0/N_sec, L*1.0/N_sec, 
    datos, plot=False )
    #Loading environment in this Z section
    eigX1 = CutFieldZ( eigV_filename+"_1", i, res=16, Coor = 1 )
    eigX2 = CutFieldZ( eigV_filename+"_2", i, res=16, Coor = 1 )
    eigX3 = CutFieldZ( eigV_filename+"_3", i, res=16, Coor = 1 )
    
    #All halos in this Z section
    for l in xrange( len(index) ):
	ind = index[l] - 1
	#y and z index
	j = abs(int(N_sec*(halos[2,ind]-0.0001)/L))
	k = abs(int(N_sec*(halos[3,ind]-0.0001)/L))
	
	#Storing eigenvalues
	eig[0,ind] = eigX1[j,k]
	eig[1,ind] = eigX2[j,k]
	eig[2,ind] = eigX3[j,k]

I = np.zeros(Nhalos)
J = np.zeros(Nhalos)
K = np.zeros(Nhalos)
for i in xrange(Nhalos):
    I[i] = abs(int(N_sec*(halos[1,i]-0.0001)/L))
    J[i] = abs(int(N_sec*(halos[2,i]-0.0001)/L))
    K[i] = abs(int(N_sec*(halos[3,i]-0.0001)/L))
    
np.savetxt( '%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,simulation,web,N_sec,smooth,catalog),
np.transpose([halos[0],eig[0],eig[1],eig[2],I,J,K]), 
fmt=('%d\t%1.5e\t%1.5e\t%1.5e\t%d\t%d\t%d') )