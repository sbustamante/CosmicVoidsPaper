#include <stdio.h>
#include <stdlib.h>
#define FLOAT1 float
#define FLOAT2 double
#define NMAX 5000

//USAGE  Density_Regions_Histogram.out <EIG_Filename> <DELTA_Filename> <Min_Lambda> <Max_Lambda> <N_Lambda> <Min_Delta> <Max_Delta> <N_Hist> <Folder>

int main(int argc, char **argv)
{    
    FILE *in, *out_hist;
    FLOAT1 *eigen1, *eigen2, *eigen3;
    FLOAT2 *delta;
    int *environment;
    char filename[100];
    
    FLOAT1 Lambda_min, Lambda_max, Lambda;
    FLOAT1 Delta_min, Delta_max;
    int N_thr, Bins;
    int j, k, eig, i_d;
    long int Ncells[NMAX], NcellsCum;
    
    //Grid variables===============================================================================
    int dumb;
    char line[30];
    long long i;
    int n_x, n_y, n_z;
    int n_nodes;
    long long n_total;
    float dx, dy, dz, x_0, y_0, z_0;
    //=============================================================================================
    
   
    //PARAMETERS===================================================================================
    //Number of divisions in Lambda_th array
    N_thr = atoi( argv[5] );
    //Minimum Lambda_th
    Lambda_min = atof( argv[3] );
    //Maximum Lambda_th
    Lambda_max = atof( argv[4] );
    //Minimum delta
    Delta_min = atof( argv[6] );
    //Maximum delta
    Delta_max = atof( argv[7] );
    //Number of bins
    Bins = atof( argv[8] );
    //=============================================================================================
        
        
    //LOADING EIGENVALUES==========================================================================
    for( eig=0; eig<3; eig++ ){
        //filename of current eigenvalue
 	sprintf(filename, "%s_%d", argv[1], eig + 1);
	if(!(in=fopen(filename, "r"))){
	    fprintf(stderr, "Problem opening file %s\n", filename);
	    exit(1);}
	fread(&dumb,sizeof(int),1,in);
	fread(line,sizeof(char)*30,1,in);
	fread(&dumb,sizeof(int),1,in);
	fread(&dumb,sizeof(int),1,in);
	fread(&n_x,sizeof(int),1,in);    
	fread(&n_y,sizeof(int),1,in);    
	fread(&n_z,sizeof(int),1,in);    
	fread(&n_nodes,sizeof(int),1,in);    
	fread(&x_0,sizeof(float),1,in);    
	fread(&y_0,sizeof(float),1,in);    
	fread(&z_0,sizeof(float),1,in);    
	fread(&dx,sizeof(float),1,in);    
	fread(&dy,sizeof(float),1,in);    
	fread(&dz,sizeof(float),1,in);    
	fread(&dumb,sizeof(int),1,in);
	n_total = n_x * n_y * n_z;
/*	fprintf(stderr, "Nx Ny Nz : %d %d %d %lld\n", n_x, n_y, n_z, n_total);
	fprintf(stderr, "x_0 y_0 z_0 : %g %g %g\n", x_0, y_0, z_0);
	fprintf(stderr, "dx dy dz : %g %g %g\n", dx, dy, dz);   */ 
	
	//First Eigenvalue
	if(eig == 0){
	    if(!(eigen1=malloc(n_nodes * sizeof(FLOAT1)))){
		fprintf(stderr, "problem with array allocation\n");
		exit(1);}
	    fread(&dumb,sizeof(int),1,in);
	    fread(&(eigen1[0]),sizeof(FLOAT1), n_total, in);
	    fread(&dumb,sizeof(int),1,in);}
	//Second Eigenvalue
	if(eig == 1){
	    if(!(eigen2=malloc(n_nodes * sizeof(FLOAT1)))){
		fprintf(stderr, "problem with array allocation\n");
		exit(1);}
	    fread(&dumb,sizeof(int),1,in);
	    fread(&(eigen2[0]),sizeof(FLOAT1), n_total, in);
	    fread(&dumb,sizeof(int),1,in);}
	//Third Eigenvalue
	if(eig == 2){
	    if(!(eigen3=malloc(n_nodes * sizeof(FLOAT1)))){
		fprintf(stderr, "problem with array allocation\n");
		exit(1);}
	    fread(&dumb,sizeof(int),1,in);
	    fread(&(eigen3[0]),sizeof(FLOAT1), n_total, in);
	    fread(&dumb,sizeof(int),1,in);}
	fclose(in);}
	
    //LOADING DENSITY FIELD========================================================================
    sprintf(filename, "%s", argv[2]);
    if(!(in=fopen(filename, "r"))){
	fprintf(stderr, "Problem opening file %s\n", filename);
	exit(1);}
    fread(&dumb,sizeof(int),1,in);
    fread(line,sizeof(char)*30,1,in);
    fread(&dumb,sizeof(int),1,in);
    fread(&dumb,sizeof(int),1,in);
    fread(&n_x,sizeof(int),1,in);    
    fread(&n_y,sizeof(int),1,in);    
    fread(&n_z,sizeof(int),1,in);    
    fread(&n_nodes,sizeof(int),1,in);    
    fread(&x_0,sizeof(float),1,in);    
    fread(&y_0,sizeof(float),1,in);    
    fread(&z_0,sizeof(float),1,in);    
    fread(&dx,sizeof(float),1,in);    
    fread(&dy,sizeof(float),1,in);    
    fread(&dz,sizeof(float),1,in);    
    fread(&dumb,sizeof(int),1,in);
    n_total = n_x * n_y * n_z;
    
    //Loading densities
    if(!(delta=malloc(n_nodes * sizeof(FLOAT2)))){
	fprintf(stderr, "problem with array allocation\n");
	exit(1);}
    fread(&dumb,sizeof(int),1,in);
    fread(&(delta[0]),sizeof(FLOAT2), n_total, in);
    fread(&dumb,sizeof(int),1,in);
        
    fclose(in);

    //HISTOGRAMS===================================================================================
    //Calculating mean and median densities and total volumes--------------------------------------
    for( j=0; j<N_thr; j++ ){
	//Initializing histograms
	for( i_d=0; i_d<Bins; i_d++ )	Ncells[i_d] = 0;
    
	//Current Lambda
	Lambda = Lambda_min + (Lambda_max - Lambda_min)*j/N_thr;
    
	//Correlation File
	sprintf(filename, "%s/delta_voids_hist_%1.2f.dat", argv[9], Lambda);
	out_hist = fopen(filename, "w");
	
	//Sweeping all the grid
	for( i=0; i<n_total; i++ ){
	    // If the cell is a void
	    if( eigen1[i] <= Lambda && eigen2[i] <= Lambda && eigen3[i] <= Lambda )
		//HISTOGRAMS
		for( i_d=0; i_d<Bins-1; i_d++ )
		    if( (delta[i] >= Delta_min + (Delta_max - Delta_min)*(i_d)/Bins) && 
			(delta[i] < Delta_min + (Delta_max - Delta_min)*(i_d+1)/Bins) ){
			Ncells[i_d] ++ ;
			break;}}
	//File Head
	fprintf( out_hist, "#\\delta\tNumber of cells\tCumulative\n");
	//Storing histogram for each eigenvalue
	NcellsCum = 0;
	for( i_d=0; i_d<Bins-1; i_d++ ){ 
	    NcellsCum += Ncells[i_d];
	    fprintf( out_hist, "%1.5f\t%ld\t%ld\n", 
		     Delta_min + (Delta_max - Delta_min)*(i_d+1)/Bins, Ncells[i_d], NcellsCum );}
	fclose( out_hist );
    }
    
    //=============================================================================================
    return 0;
}