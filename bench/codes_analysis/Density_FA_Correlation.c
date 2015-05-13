#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define FLOAT1 float
#define FLOAT2 double
#define NMAX1 1000

//Usage  Density_FA_Correlation.out <eig_filename> <delta_filename> <Delta min> <Delta max> <number of Delta bins>
// 			       <FA min> <FA max> <number of FA bins>

float FA( float eig1, float eig2, float eig3 )
{ 
    float fa;
    fa = (1/pow(3,0.5))*pow( ( pow(eig1 - eig3,2) + pow(eig2 - eig3,2) + pow(eig1 - eig2,2) )/ \
    (eig1*eig1 + eig2*eig2 + eig3*eig3), 0.5 );
    return fa;
}

int main(int argc, char **argv)
{   
    FILE *in, *out_count;
    FLOAT1 *eigen1, *eigen2, *eigen3;
    FLOAT2 *delta;
    char filename[100];
    int eig;
    
    float delta_min, delta_max, FA_min, FA_max;
    int N_FA, N_delta, i_lm, i_fa;
    float count[NMAX1][NMAX1];
    float fa, d, fa_f, d_f, fa_i, d_log;
    
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
    delta_min = atof( argv[3] );
    delta_min = log10(delta_min+1);
    delta_max = atof( argv[4] );
    delta_max = log10(delta_max+1);
    //Number of divisions in Lambda
    N_delta = atoi( argv[5] );
    //FA Range
    FA_min = atof( argv[6] );
    FA_max = atof( argv[7] );
    //Number of divisions in FA
    N_FA = atoi( argv[8] );
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

    //Initializing counters
    for( i_lm=0; i_lm<N_delta; i_lm++ )
	for( i_fa=0; i_fa<N_FA; i_fa++ )
	    count[i_lm][i_fa] = 0.0;
	
    for( i=0; i<n_total; i++ ){
	fa_i = FA( eigen1[i], eigen2[i], eigen3[i] );
	for( i_lm=0; i_lm<N_delta; i_lm++ ){	    
	    //current lambda bin
	    d = delta_min+ + (delta_max-delta_min)*i_lm/N_delta;
	    //Next lambda bin
	    d_f = delta_min+ + (delta_max-delta_min)*(i_lm+1)/N_delta;
	    d_log = log10(delta[i]+1);
	    if( d_log>=d && d_log<d_f ){
		for( i_fa=0; i_fa<N_FA; i_fa++ ){
		    //current fa bin
		    fa = FA_min + (FA_max-FA_min)*i_fa/N_FA;
		    //Next fa bin
		    fa_f = FA_min + (FA_max-FA_min)*(i_fa+1)/N_FA;
		    //If the current cell is within such void
		    if( fa_i>=fa && fa_i<fa_f ){
			count[i_lm][i_fa] ++;
			break;}}
		break;}}}

	    
    //File Head
    out_count = fopen("temp.tmp", "w");
    for( i_lm=0; i_lm<N_delta; i_lm++ ){
	for( i_fa=0; i_fa<N_FA; i_fa++ )
	    fprintf( out_count, "%1.5e\t", count[i_lm][i_fa] );
	fprintf( out_count,"\n" );}
	
    fclose(out_count);	
    //=============================================================================================
    return 0;
}