#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define FLOAT1 float
#define FLOAT2 double
#define NMAX1 1000

//Usage  Density_L3_Correlation.out <eig_filename> <delta_filename> <Lambda min> <Lambda max> 
// 				    <number of lambda bins> <delta min> <delta max> <number of delta bins>

int main(int argc, char **argv)
{   
    FILE *in, *out_count;
    FLOAT1 *eigen1, *eigen2, *eigen3;
    FLOAT2 *delta;
    char filename[100];
    int eig;
    
    float lambda_min, lambda_max, delta_min, delta_max;
    int N_delta, N_lambda, i_lm, i_delta;
    float count[NMAX1][NMAX1];
    float lamb, lamb_f;
    double delta_f, delta_i;
    
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
    //Lambdas Range
    lambda_min = atof( argv[3] );
    lambda_max = atof( argv[4] );
    //Number of divisions in Lambda
    N_lambda = atoi( argv[5] );
    //Delta Range
    delta_min = atof( argv[6] );
    delta_max = atof( argv[7] );
    //Number of divisions in delta
    N_delta = atoi( argv[8] );
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
	fprintf(stderr, "dx dy dz : %g %g %g\n", dx, dy, dz);  */  
	
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
    
    //Loading densities
    if(!(delta=malloc(n_nodes * sizeof(FLOAT2)))){
	fprintf(stderr, "problem with array allocation\n");
	exit(1);}
    fread(&dumb,sizeof(int),1,in);
    fread(&(delta[0]),sizeof(FLOAT2), n_total, in);
    fread(&dumb,sizeof(int),1,in);
    

    //HISTOGRAMS===================================================================================
    
    //Initializing counters
    for( i_lm=0; i_lm<N_lambda; i_lm++ )
	for( i_delta=0; i_delta<N_delta; i_delta++ )
	    count[i_lm][i_delta] = 0.0;
	
    for( i=0; i<n_total; i++ ){
	for( i_lm=0; i_lm<N_lambda; i_lm++ ){	    
	    //current lambda bin
	    lamb = lambda_min + (lambda_max-lambda_min)*i_lm/N_lambda;
	    //Next lambda bin
	    lamb_f = lambda_min + (lambda_max-lambda_min)*(i_lm+1)/N_lambda;
	    if( eigen1[i]>=lamb && eigen1[i]<lamb_f ){
		for( i_delta=0; i_delta<N_delta; i_delta++ ){
		    //current delta bin
		    delta_i = delta_min + (delta_max-delta_min)*i_delta/N_delta;
		    //Next delta bin
		    delta_f = delta_min + (delta_max-delta_min)*(i_delta+1)/N_delta;
		    //If the current cell is within such void
		    if( delta[i]>=delta_i && delta[i]<delta_f ){
			count[i_lm][i_delta] ++;
			break;}}
		break;}}}

	    
    //File Head
    out_count = fopen("temp.tmp", "w");
    for( i_lm=0; i_lm<N_lambda; i_lm++ ){
	for( i_delta=0; i_delta<N_delta; i_delta++ )
	    fprintf( out_count, "%1.5e\t", count[i_lm][i_delta] );
	fprintf( out_count,"\n" );}
	
    fclose(out_count);	
    //=============================================================================================
    return 0;
}