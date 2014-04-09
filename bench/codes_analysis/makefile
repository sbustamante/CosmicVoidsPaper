#==============================================================================
#	THE PLACE OF THE LOCAL GROUP IN THE COSMIC WEB
#==============================================================================
# Sebastian Bustamante (Universidad de Antioquia), macsebas33@gmail.com
# Jaime Forero-Romero (Universidad de los Andes)

#C Compiler
COMPILER = gcc

compile:
		$(COMPILER) Field_Cut16.c -o Field_Cut16.out
		$(COMPILER) Field_Cut32.c -o Field_Cut32.out
		$(COMPILER) void_matrix_builder.c -o void_matrix_builder.out
		$(COMPILER) Density_Regions.c -o Density_Regions.out
		$(COMPILER) Void_Regions_Histogram.c -o Void_Regions_Histogram.out
		$(COMPILER) Lambda_Histograms_Variance.c -o Lambda_Histograms_Variance.out
		$(COMPILER) Lambda_Histograms.c -o Lambda_Histograms.out

clean:
		rm -f *.out
		