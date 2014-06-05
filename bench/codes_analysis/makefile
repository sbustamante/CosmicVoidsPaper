#==============================================================================
#	THE PLACE OF THE LOCAL GROUP IN THE COSMIC WEB
#==============================================================================
# Sebastian Bustamante (Universidad de Antioquia), macsebas33@gmail.com
# Jaime Forero-Romero (Universidad de los Andes)

#C Compiler
COMPILER = gcc

compile:
		$(COMPILER) Field_Cut16.c -o Field_Cut16.out
		@echo -e
		$(COMPILER) Field_Cut32.c -o Field_Cut32.out
		@echo -e
		$(COMPILER) void_matrix_builder.c -o void_matrix_builder.out
		@echo -e
		$(COMPILER) Density_Regions.c -o Density_Regions.out
		@echo -e
		$(COMPILER) Density_Regions_Histogram.c -o Density_Regions_Histogram.out
		@echo -e
		$(COMPILER) Lambda_Histograms_Variance.c -o Lambda_Histograms_Variance.out
		@echo -e
		$(COMPILER) Lambda_Histograms.c -o Lambda_Histograms.out
		@echo -e
		$(COMPILER) FA_L1_Correlation.c -lm -o FA_L1_Correlation.out
		@echo -e
		$(COMPILER) Density_L1_Correlation.c -lm -o Density_L1_Correlation.out
		@echo -e
		$(COMPILER) Central_Voids_Properties.c -lm -o Central_Voids_Properties.out
		@echo -e
		$(COMPILER) Density_Classification.c -lm -o Density_Classification.out
		@echo -e

clean:
		rm -f *.out
		