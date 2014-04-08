#include <stdio.h>
#include <stdlib.h>
#define FLOAT1 float
#define FLOAT2 double
#define NMAX 1000

//USAGE  Density_Regions.out <EIG_Filename> <DELTA_Filename> <Min_Lambda> <Max_Lambda> <N_Lambda> <Out_Filename>

int main(int argc, char **argv)
{    
    FILE *in, *out_corr;
    FLOAT1 *eigen1, *eigen2, *eigen3;
    FLOAT2 *delta;
    int *environment;
    char filename[100];
    
    FLOAT1 Lambda_min, Lambda_max, Lambda;
    int j, k, N_thr, eig;
    float Nrho[NMAX][4];
    int Nreg[NMAX][4];
    
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
    //Minim Lambda_th
    Lambda_min = atof( argv[3] );
    //Maxim Lambda_th
    Lambda_max = atof( argv[4] );
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
/*    fprintf(stderr, "Nx Ny Nz : %d %d %d %lld\n", n_x, n_y, n_z, n_total);
    fprintf(stderr, "x_0 y_0 z_0 : %g %g %g\n", x_0, y_0, z_0);
    fprintf(stderr, "dx dy dz : %g %g %g\n", dx, dy, dz); */   
    
    if(!(delta=malloc(n_nodes * sizeof(FLOAT2)))){
	fprintf(stderr, "problem with array allocation\n");
	exit(1);}
    fread(&dumb,sizeof(int),1,in);
    fread(&(delta[0]),sizeof(FLOAT2), n_total, in);
    fread(&dumb,sizeof(int),1,in);
    
    fclose(in);

    //CORRELATIONS=================================================================================
    //Correlation File
    sprintf(filename, "%s", argv[6]);
    out_corr=fopen(filename, "w");

    //Initializing histograms
    for( j=0; j<N_thr; j++ )
	for( i=0; i<4; i++ ){
	    Nrho[j][i] = 0;
	    Nreg[j][i] = 0;}
    
    for( j=0; j<N_thr; j++ ){

	for( i=0; i<n_total; i++ ){
	//Current Lambda
	Lambda = Lambda_min + (Lambda_max - Lambda_min)*j/N_thr;
	
	//HISTOGRAMS
	// voids
	if( eigen1[i] <= Lambda && eigen2[i] <= Lambda && eigen3[i] <= Lambda ){
	    Nreg[j][0] ++;
	    Nrho[j][0] += delta[i];}
	// sheets    
	if( eigen1[i] > Lambda && eigen2[i] <= Lambda && eigen3[i] <=  Lambda ){
	    Nreg[j][1] ++;
	    Nrho[j][1] += delta[i];}
	// filaments    
	if( eigen1[i] > Lambda && eigen2[i] >  Lambda && eigen3[i] <=  Lambda ){
	    Nreg[j][2] ++;
	    Nrho[j][2] += delta[i];}
	// knots
	if( eigen1[i] >  Lambda && eigen2[i] >  Lambda && eigen3[i] >  Lambda ){
	    Nreg[j][3] ++;
	    Nrho[j][3] += delta[i];}
    }}

    //File Head
    fprintf( out_corr, "#Lamb\t\tDrg1\t\tDrg2\t\tDrg3\t\tDrg4\t\tN1\t\tN2\t\tN3\t\tN4\t\tNtot\n");
    for( j=0; j<N_thr; j++ ){
      	//Current Lambda
	Lambda = Lambda_min + (Lambda_max - Lambda_min)*j/N_thr;
	
	fprintf( out_corr, "%1.3f\t%1.5e\t%1.5e\t%1.5e\t%1.5e\t%8d\t%8d\t%8d\t%8d\t%8d\n", Lambda, \
        Nrho[j][0], Nrho[j][1], Nrho[j][2], Nrho[j][3],
	Nreg[j][0], Nreg[j][1], Nreg[j][2], Nreg[j][3],
	Nreg[j][0] + Nreg[j][1] + Nreg[j][2] + Nreg[j][3]);}
	
    fclose(out_corr);	
    
    //=============================================================================================
    return 0;
}