COSMIC VOIDS
==============================================
**Sebastian Bustamante**
*(Universidad de Antioquia)*

**Jaime Forero-Romero**
*(Universidad de los Andes)*


Description
-----------------------------------------------------------------------------------------
Finding and characterizing underdense regions (voids) in the large scale structure of the 
Universe is an important task in cosmological studies. In this paper we present a new 
algorithm to find voids in cosmological simulations. Our approach is based on algorithms 
that use the tidal and the velocity shear tensors to locally define the cosmic web.
Voids are identified using the fractional anisotropy (FA) computed from the eigenvalues 
of each web scheme. We define the void boundaries using a watershed transform based on the
local minima of the FA and its boundaries as the regions where the FA is maximized.
This void identification technique does not have any free parameters and does not make any 
assumption on the shape or structure of the voids. We test the method on the Bolshoi 
simulation and report on the density and velocity profiles for the voids found using this 
new scheme. 


Results
-----------------------------------------------------------------------------------------
All results in this paper can be reproduced with codes and data in the folder bench/codes 
and with [these](http://goo.gl/B9pYxU) data. Furthermore you can use [this](http://nbviewer.ipython.org/urls/raw.githubusercontent.com/sbustamante/CosmicVoidsPaper/master/bench/analysis.ipynb?create=1) 
ipython notebook in order to reproduce figures.
