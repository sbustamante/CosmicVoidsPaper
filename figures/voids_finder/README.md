COSMIC VOIDS: visual impressions of void schemes
==============================================
**Sebastian Bustamante**
*(Universidad de Antioquia)*

**Jaime Forero-Romero**
*(Universidad de los Andes)*


Here it is presented some results obtained with the three scheme used for
void finding. Each figure presents three panels, the first one corresponds 
to an slide of the field used for the watershed transform (density field or
fractional anisotropy for T-web or V-web). The second panel shows the visual
impression obtained for each type of environment (voids, sheets, filaments 
and peaks). The third panel shows all the individual void regions found by
each scheme, each void is coloured in order to differenciate it from its 
neighbours.

The three schemes are:

-	density: void finder through a watershed transform of the density field
-	FA-Tweb: void finder based on the watershed transform of the FA field as calculated from Tweb eigenvalues
-	FA-Vweb: void finder based on the watershed transform of the FA field as calculated from Vweb eigenvalues

Furthermore, for each scheme it is performed a median filtering in order to
reduce short noise. The first number refers to the order or the median filtering
(how many times it is applied over the field). Finally, it is also applied a 
boundary removal procedure, where voids that share a boundary with a mean value
above a threshold value are merged (it implies that the barrier in between is not
deep enough in order to have separated voids). The applying of this procedure is
indicated by the last number. For example:

*cosmicweb_FA_Tweb_00.png*

That is the result of the FA-Tweb watershed scheme, without median filtering and
without boundary removal.

*cosmicweb_density_21.png*

This is the result of the density watershed scheme, with a 2nd-order median filtering
(median filtering applied two times), and with boundary removal activate.