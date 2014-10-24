#halos_fraction.py
#
#This code calculates plots of fraction of halos in each one of the defined environments for a 
#range od threshold values
#Usage: halos_fraction.py <Vweb or Tweb> <FAG or DLG> <BDM or FOF> <show(0) or save(1)>
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
#Voids scheme
voids = sys.argv[2]
#Web Scheme
web = sys.argv[1]
#Catalogue
catalog = sys.argv[3]
#Colors
colors = {"voids":"navy", "sheets":"yellowgreen", "filaments":"orangered", "knots":"c"}
#Bins for masses
Nbins = 20
#Mass ranges
Mmin = 10**(10.5)
Mmax = 1e15

#Values to evaluate lambda_th
if web == 'Tweb':
    Lambda_opt = 0.265
if web == 'Vweb':
    Lambda_opt = 0.175
if voids == "DLG":
    th_vd = -0.57
    th_sh = 0.60
    th_fl = 8.82

#==================================================================================================
#			Fraction of halos in each environment for different masses
#==================================================================================================

plt.figure( figsize=(5,5) )

#Loading density filename
rho_filename = '%s%s%s/%d/Delta%s'%(foldglobal,simulation,"Tweb",N_sec,smooth)

#Loading Properties of halos
masses = np.transpose(np.loadtxt('%s%s/C_GH_%s.dat'%(foldglobal,simulation, catalog)))[8]
eigs = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,simulation,web,N_sec,smooth,catalog)))
rho = np.transpose(np.loadtxt('%s%s%s/%d/D_GH%s_%s.dat'%(foldglobal,simulation,"Tweb",N_sec,smooth,catalog)))[1]

#Making histograms
Voids_hist = np.zeros(Nbins)
Sheet_hist = np.zeros(Nbins)
Filam_hist = np.zeros(Nbins)
Knots_hist = np.zeros(Nbins)
M_array = 10**np.linspace( np.log10(Mmin), np.log10(Mmax), Nbins+1 )

if voids == "DLG":
    for i in xrange( Nbins ):
	rhoi = rho[ (M_array[i]<= masses)*(masses< M_array[i+1]) ]
	print len(rhoi)
	Voids_hist[i] = np.sum( rhoi<=th_vd )/(1.0*len(rhoi))
	Sheet_hist[i] = np.sum( (rhoi>th_vd)*(rhoi<=th_sh) )/(1.0*len(rhoi))
	Filam_hist[i] = np.sum( (rhoi>th_sh)*(rhoi<=th_fl) )/(1.0*len(rhoi))
	Knots_hist[i] = np.sum( rhoi>th_fl )/(1.0*len(rhoi))
	
if voids == "FAG":
    for i in xrange( Nbins ):
	eigsi = eigs[ :, (M_array[i]<= masses)*(masses< M_array[i+1]) ]
	Knots_hist[i] = np.sum( (eigsi[1]>Lambda_opt)*(eigsi[2]>Lambda_opt)*(eigsi[3]>Lambda_opt) )/(1.0*len(eigsi[0]))
	Filam_hist[i] = np.sum( (eigsi[1]>Lambda_opt)*(eigsi[2]>Lambda_opt)*(eigsi[3]<=Lambda_opt) )/(1.0*len(eigsi[0]))
	Sheet_hist[i] = np.sum( (eigsi[1]>Lambda_opt)*(eigsi[2]<=Lambda_opt)*(eigsi[3]<=Lambda_opt) )/(1.0*len(eigsi[0]))
	Voids_hist[i] = np.sum( (eigsi[1]<=Lambda_opt)*(eigsi[2]<=Lambda_opt)*(eigsi[3]<=Lambda_opt) )/(1.0*len(eigsi[0]))
	
#Plotting knots
plt.fill_between( M_array[:-1], np.zeros(Nbins), Knots_hist, color=colors["knots"] )
plt.fill_between( M_array[:-1], Knots_hist, Knots_hist+Filam_hist, color=colors["filaments"] )
plt.fill_between( M_array[:-1], Knots_hist+Filam_hist, Knots_hist+Filam_hist+Sheet_hist, color=colors["sheets"] )
plt.fill_between( M_array[:-1], Knots_hist+Sheet_hist+Filam_hist, Knots_hist+Sheet_hist+Filam_hist+Voids_hist, color=colors["voids"] )
plt.semilogx([0,],[0,])

#plt.ylim( (0,1) )
plt.xlim( (Mmin,Mmax) )
plt.show()