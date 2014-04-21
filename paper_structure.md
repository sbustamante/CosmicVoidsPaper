COSMIC VOIDS: paper structure
=========================================================================================

**Sebastian Bustamante**
*(Universidad de Antioquia)*

**Jaime Forero-Romero**
*(Universidad de los Andes)*


1. Introduction
-----------------------------------------------------------------------------------------
Brief introduction to the problem of voids in a cosmological context. Bibliography review
and recent relevants works.


2. The simulation
-----------------------------------------------------------------------------------------
Technical details of the used simulation (Bolshoi), with descriptions of halos 
catalogues (BDM and FOF). All halo samples are defined here as well.


3. Algorithms to quantify the cosmic web
-----------------------------------------------------------------------------------------
Detailed description of each web classification scheme (V-web and T-web). Furthermore, it
is presented a nowel approximation to select an optimal threshold parameter by using mean 
(median?) densities of sheet (void?) regions.


4. Finding bulk voids
-----------------------------------------------------------------------------------------
Here, it is presented a FOF-like scheme used to find bulk void regions, where each void
cell catalogued as a void by the web scheme and the optimal threshold parameter is used 
as an input "particle" in the FOF algorithm. To optimize this scheme, a percolation 
analysis is also performed in order to reduce this numerical phenomenon, where a null
threshold parameter is found to be the best way to overcome percolation. Next, it is 
proposed a new squeme to classify bulk voids that minimizes percolation. This consists in
taking a seed catalogue of voids (it could be the FOF catalogue of voids for a lambda_th
null), and then make each void grow up from consecutive layers until all void cells are
catalogue in a bulk void.


5. Properties of voids
-----------------------------------------------------------------------------------------
Throghout this section is presented a classification of voids according to their shape, 
this is reached by using the reduced intertia tensor and the respective eigenvalues. it
is found, completely anisotropic voids are preferred in the LCDM cosmological model. 
Besides we make an extensive analysis of density profiles and density of dark matter halos
as radial functions (elliptical approximation?).


6. Statistics of voids and influence over dark matter halos
-----------------------------------------------------------------------------------------
Here, it is performed an analysis over the influence of voids over the physical properties
of dark matter halos, like their mass or their spin parameter. It is found dark matter 
halos are preferentially distributed near to large volume voids, while a minor fraction of 
them are relatively further to smaller bulk voids. It is also included (?) an analysis of 
other physical properties like MAH history and number of satellite halos.


7. Conclusions
-----------------------------------------------------------------------------------------
Summarizing main results and conclusions


8. Acknowledges
-----------------------------------------------------------------------------------------
bla bla bla
