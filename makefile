#==============================================================================
#	COSMIC VOIDS
#==============================================================================
# Sebastian Bustamante (Universidad de Antioquia), macsebas33@gmail.com
# Jaime Forero-Romero (Universidad de los Andes)

#Commit mesage to update in git repo
MSG = "Last commit"
#Name of tex file
FILE_TEX  = cosmic_voids
#Latex compiler
LATEX = pdflatex
#Viewer of pdf files
VIEWER = okular
#Latex editor
TEXEDIT = texmaker
#Current date
DATESTAMP=`date +'%Y-%m-%d'`
#Bench
BENCH = bench
#Folder of Codes for Analysis
ACODESFOLD = codes_analysis
#Folder of Codes for Figures
FCODESFOLD = codes_figures
#Folder of data for Figures
DATAFOLD = data_figures


pdflatex:	$(FILE_TEX).tex  
		$(LATEX) $(FILE_TEX).tex 
		bibtex ${FILE_TEX}
		$(LATEX) $(FILE_TEX).tex 
		$(LATEX) $(FILE_TEX).tex 



clean:
		rm -f $(FILE_TEX).aux
		rm -f $(FILE_TEX).out
		rm -f $(FILE_TEX).bbl
		rm -f $(FILE_TEX).log
		make -C bench/codes clean

view: 
		$(VIEWER) $(FILE_TEX).pdf &

edit:
		$(TEXEDIT) $(FILE_TEX).tex &

update:
		git add 			\
		./figures/* 			\
		cosmic_voids.tex		\
		cosmic_voids.pdf		\
		makefile			\
		./latex/mn2e.bst		\
		./latex/mn2e.cls		\
		references.bib			\
		README.md				\
		./latex/macros.tex		\
		./bench/codes_analysis/*.py	\
		./bench/codes_analysis/*.c	\
		./bench/codes_figures/*.py	\
		./bench/codes_figures/*.c	\
		./bench/data_figures/*
	
compile:
		make -C $(CODESFOLD) compile

help:
		@echo -e 'Makefile Help:'
		@echo -e '\tpdflatex:\t compile the pdf file'
		@echo -e '\tclean:\t\t clean all temporal files'
		@echo -e '\tview:\t\t view the pdf file with standard viewer ($(VIEWER))'
		@echo -e '\tedit:\t\t edit the tex file with standard editor ($(TEXEDIT))'
		@echo -e '\tupdate:\t\t update all files to github repository'
		@echo -e '\tcompile:\t compile the required c codes in $(ACODESFOLD) and $(FCODESFOLD)'
		@echo -e '\thelp:\t\t this help!'