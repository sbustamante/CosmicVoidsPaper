execfile('_Head.py')
from mayavi import mlab as mlab
import moviepy.editor as mpy

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
simulation = "BOLSHOI/"
#Number of sections
N_sec = 256
#Box lenght [Mpc]
L_box = 250.
#Smooth parameter
smooth = '_s1'
#Web Scheme
web = "Tweb"
#Void finder scheme (FAG or DLG)
void_scheme = "FAG"
#Configuration 
config = "01"
#Duration of GIFS [2]
duration = 2
#Void to plot
IDvoid = int(sys.argv[1])

datos = np.loadtxt("%s/%s/%s/%d/voids%s/voids_%s/void_index.dat"%\
(foldglobal, simulation, web, N_sec, void_scheme, config ))
datos = datos.reshape( (256,256,256) )

radius = (np.loadtxt("%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%\
(foldglobal, simulation, web, N_sec, void_scheme, config ), ))**(1/3.0)
radius = radius[:,1]

def void(i, figure, show = False):
    datos2 = np.copy(datos)
    datos2[datos!=i] = 0
    contour = mlab.contour3d(datos2, contours=2)
    #mlab.pipeline.volume(mlab.pipeline.scalar_field(datos), vmin=0)
    if show:
	mlab.show()
    return contour
    
    
#==================================================================================================
#			CREATING GIFS
#==================================================================================================
#Generating figure
fig = mlab.figure(size=(500, 500), bgcolor=(0,0,0))
contour = void(IDvoid, fig)

def make_frame(t):
    """ Generates and returns the frame for time t. """
    mlab.view(azimuth= 360*t/duration, distance=6*radius[IDvoid]) # camera angle
    return mlab.screenshot(antialiased=True) # return a RGB image

animation = mpy.VideoClip(make_frame, duration=duration).resize(0.5)
# Video generation takes 10 seconds, GIF generation takes 25s
animation.write_videofile("wireframe.mp4", fps=20)
animation.write_gif("wireframe.gif", fps=20)