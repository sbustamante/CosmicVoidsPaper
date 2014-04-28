#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define FLOAT1 float
#define NMAX1 1000

//Usage  FA_L1_Correlation.out <eig_filename> <Lambda min> <Lambda max> <number of lambda bins>
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
    char filename[100];
    int eig;
    
    float lambda_min, lambda_max, FA_min, FA_max;
    int N_FA, N_lambda, i_lm, i_fa;
    float count[NMAX1][NMAX1];
    float fa, lamb, fa_f, lamb_f, fa_i;
    
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
    lambda_min = atof( argv[2] );
    lambda_max = atof( argv[3] );
    //Number of divisions in Lambda
    N_lambda = atoi( argv[4] );
    //FA Range
    FA_min = atof( argv[5] );
    FA_max = atof( argv[6] );
    //Number of divisions in FA
    N_FA = atoi( argv[7] );
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

    //Initializing counters
    for( i_lm=0; i_lm<N_lambda; i_lm++ )
	for( i_fa=0; i_fa<N_FA; i_fa++ )
	    count[i_lm][i_fa] = 0.0;
	
    for( i=0; i<n_total; i++ ){
	fa_i = FA( eigen1[i], eigen2[i], eigen3[i] );
	for( i_lm=0; i_lm<N_lambda; i_lm++ ){	    
	    //current lambda bin
	    lamb = lambda_min + (lambda_max-lambda_min)*i_lm/N_lambda;
	    //Next lambda bin
	    lamb_f = lambda_min + (lambda_max-lambda_min)*(i_lm+1)/N_lambda;
	    if( eigen1[i]>=lamb && eigen1[i]<lamb_f ){
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
    for( i_lm=0; i_lm<N_lambda; i_lm++ ){
	for( i_fa=0; i_fa<N_FA; i_fa++ )
	    fprintf( out_count, "%1.5e\t", count[i_lm][i_fa] );
	fprintf( out_count,"\n" );}
	
    fclose(out_count);	
    //=============================================================================================
    return 0;
}