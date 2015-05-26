Conceptual:
==

1. **It seems that part of the motivation for using FA is that it is very well correlated with lambda_1, 
    at low lambda_1. FA is a rather interesting quantity in itself, differentiating haloes and voids from 
    filaments and walls, but it is not clear why it should be superior to lambda_1 for void finding. The 
    authors should more clearly articulate why this might be, if there is a reason. The FA being "conceived 
    to quantify the anisotropy of the diffusivity of water molecules through cerebral tissue in nuclear 
    magnetic resonance imaging" should be elaborated on; this does not clarify the usefulness of the FA for 
    cosmologists. Conceptually, I also wonder: do filaments and walls behave differently from each other in 
    FA, or do they both have FA ~ 1?**

      Response: 
      - Although lambda_1 is the defining property of voids when using the T-web/V-web (1st paragraph of 
	subsec 3.2), the FA exihibit a key advantage that makes it a better void tracer (please refer to 
	3rd paragraph of subsec. 3.2 of the new version).
      - Now it is explicitly explained why the FA, as defined in the context of MRI, is useful to cosmologist 
	(6th paragraph of introduction and 1st paragraph of subsec 3.1).
      - A new figure (Fig 3.) was prepared. Histograms of the volume contribution of each environment for 
	each value of the FA (3rd paragraph of subsec. 3.2). Sheets (mainly) and filaments are clearly 
	associated with high values of the FA.
      

2. **I did not understand the sentence at the end of Sect 2, "In this work we propose an optimal value of 
    the threshold based on the maximization of the fractional anisotropy field in the locations label[ed] 
    as filaments and walls," and this seems to be an important point. Is the threshold mentioned in this 
    sentence a threshold in lambda_1, or FA? Is this the 0.95 threshold in FA? It seems to be a reasonable 
    choice, but I do not see a sense in which it is "optimal," except that it seems to be the boundary 
    between the FA being well-correlated with lambda_1 and not-so-well. Also, if this sentence is about the 
    0.95 threshold, I do not see why it "does not enter into our computations," since the boundary of many 
    voids will depend on this threshold. It would be useful to know for what fraction of voids the limit 
    FA = 0.95 actually affects the boundary (in the case of the largest voids, I suppose).**

    
3. **I do not see how the value of FA=0.65 (corresponding to lambda_1 = 0) is used "to remove ridges."**

    Response: 
    - We have added a clearer explanation of the ridge removing procedure (3rd paragraph of subsec. 3.3).

    
4. **In Fig. 6, I only see a clear ridge in FA at r~r_eff in a few cases. the sentence in Sect. 5.5 "The 
    difference between the radius where the density ridge is reached ([r/]reff = 3) and the radius of the 
    FA ridge ([r/]reff = 1 ) ..." implies that I should see a ridge in FA at r~r_eff. Is this because the 
    ridge is actually a 2D surface that is spherically averaged? It would be helpful to point this (or any 
    other reasons) out. Also, the statement "This makes the FA ridge a reasonable boundary for voids compared 
    to the traditional definition that puts the boundary at the density ridge" implies (perhaps 
    unintentionally) that the FA ridge is a superior marker of the edge of a void than a density ridge. It is 
    a physically different sort of ridge, and I agree that it is reasonable, but I do not see why it should 
    be superior.**

    
5. **I am not convinced that the "tiny white bubbles located inside sheets" are embedded in overdense regions. 
    Based just on Fig. 1, they could be physical, but small, voids. We also no nothing of their extent 
    perpendicular to the plane of Fig. 1; we could just be looking of corners of much larger objects.**
    
    Response:
    - In Right panels of Fig. 1, the color of each void refers now the effective radius. The size can now be
      inferred from the figure. Small voids are indeed located inside sheets and filaments.
 
 
6. **2D histograms of (lambda_1, delta) and (lambda_1, FA) are shown in Fig. 2, and I would appreciate also 
    seeing a (FA, delta) 2D histogram, maybe with 1+delta on a log scale, which would help to clarify the 
    physical meaning of FA.**
    
    Response: 
    - The requested histogram has been added as the bottom panel of Fig. 2. This shows that lower values of
      the FA are associated to small (voids) and large values (clusters) of the density.

      
More minor things:
==

7. **I'm confused a bit about the middle panels of Fig. 1. The title,
    "Visual impresion for lambda_th=..."  is strange. Aren't there
    several thresholds here? Also, what are the blue dots? Also
    "impresion" is  misspelled.**
    
    Response:
    - We have rewritten the caption. There are two different
    thresholds, one for each web finder. Blue dots were dark matter
    halos (FOF). We removed them for clarity. The typo ("impresion")
    is  also corrected.  

      
8. **Sect 3.3, 2nd paragraph: I do not see why "the analysis of [y]our
    results" shows that a fixed Cartesian  mesh does not induce
    spurious results". It's true, that the results look reasonable,
    but I think it would  be better to state something about the level
    of discreteness noise, e.g. the number of zero-density cells,  or
    the minimum if there are none.** 

    Response:
    We have rephrased this in terms of the number of particles per
    cell in the lowest density regions.

    
9. **Sect. 5.4: The sentence "subcompensated voids have outflowing ve-
    locity profiles all the way up to the effective radius where the
    average radial density reaches the average value" is a bit
    confusing; this is not r_eff, right? If so, this statement seems
    to be an understatement (v_r >0 out to several r_eff,
    typically). If not, "effective" should be removed for clarity.** 

    Response:
    We removed "effective" for clarity.

    
10. **In Sect. 5.5, there are a few instances where I think you meant "r/r_eff =" instead of "r_eff =".**


11. **All quantities are computed at the pixel scale, ~1 Mpc/h, correct? If the authors have any insights about 
    how the results would change if this scale were changed, it would be helpful to state them. A quantitative 
    discussion of how some results would change with a different scale would be great, but not necessary.**

    
12. **Finally, about the necessity of color: Figs 4-6, as they currently are, require color, but it would be 
    easy for the authors to use different linestyles, as well, to make color unnecessary.**
    
    Response:
    - These figures have already different linewidths for each bin. We think it might be easier to have 6 
      different widths than 6 different linestyles.