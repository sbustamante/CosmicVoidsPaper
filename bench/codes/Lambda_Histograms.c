#include <stdio.h>
#include <stdlib.h>
#define FLOAT1 float
#define NMAX1 1000
#define NMAX2 10000

//Usage  Lambda_Histogram.out <eig_filename> <size of 2D hist> <size of 1D hist> <Lambda range> <Histogram Type>
// Histogram Type
//	0	L1
//	1	L2
//	2	L3
//	3	L1 - L2
//	4	L1 - L3

int main(int argc, char **argv)
{   
    FILE *in, *out_count;
    FLOAT1 *eigen1, *eigen2, *eigen3;
    char filename[100];
    float Lambda_ex, L1, L2, L3;
    
    int l, m, n, N_2C, N_1C, eig, l2, m2, n2;
    int count13[NMAX1][NMAX1], count12[NMAX1][NMAX1];
    int countL1[NMAX2], countL2[NMAX2], countL3[NMAX2];

    
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
    //Number of divisions in Lambda count
    N_2C = atoi( argv[2] );     
    N_1C = atoi( argv[3] );     
    //Lambdas Range
    Lambda_ex = atof( argv[4] );
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
	

    //EIGENVALUES COUNT============================================================================
    //Output File
    sprintf(filename, "temp.tmp");
    out_count=fopen(filename, "w");

    for( l=0; l<N_1C; l++ ){
	countL1[l] = 0;
	countL2[l] = 0;
	countL3[l] = 0;}
    
    //Initializing counts
    for( l=0; l<N_2C; l++ )
	for( m=0; m<N_2C; m++ ){
	    count13[l][m] = 0;
	    count12[l][m] = 0;}

    //Building the histograms of eigenvalues counts
    for( i=0; i<n_total; i++ ){
	//1D Histograms
	l = (int)( N_1C*(eigen1[i] + Lambda_ex)/(2*Lambda_ex) );
	m = (int)( N_1C*(eigen2[i] + Lambda_ex)/(2*Lambda_ex) );
	n = (int)( N_1C*(eigen3[i] + Lambda_ex)/(2*Lambda_ex) );
	countL1[l] ++ ;
	countL2[m] ++ ;
	countL3[n] ++ ;

	//2D Histograms
	l2 = (int)( N_2C*(eigen1[i] + Lambda_ex)/(2*Lambda_ex) );
	m2 = (int)( N_2C*(eigen2[i] + Lambda_ex)/(2*Lambda_ex) );
	n2 = (int)( N_2C*(eigen3[i] + Lambda_ex)/(2*Lambda_ex) );
	count13[l2][n2] ++ ;
	if( eigen3[i] <= 0 )
	    count12[l2][m2] ++ ;

    }
    // L1 Distribution
    if( atoi(argv[5]) == 0 )
	for( l=0; l<N_1C; l++ ){
	  L1 = -Lambda_ex + ( 2*Lambda_ex )*l/N_1C;
	  fprintf( out_count, "%1.3e\t%d\n", L1, countL1[l] );}
	  
    // L2 Distribution
    if( atoi(argv[5]) == 1 )
	for( l=0; l<N_1C; l++ ){
	  L2 = -Lambda_ex + ( 2*Lambda_ex )*l/N_1C;
	  fprintf( out_count, "%1.3e\t%d\n", L2, countL2[l] );}
	  
    // L3 Distribution
    if( atoi(argv[5]) == 2 )
	for( l=0; l<N_1C; l++ ){
	  L3 = -Lambda_ex + ( 2*Lambda_ex )*l/N_1C;
	  fprintf( out_count, "%1.3e\t%d\n", L3, countL3[l] );}

    // L1 - L2  Distribution
    if( atoi(argv[5]) == 3 )
 	for( l=0; l<N_2C; l++ ){
	    for( m=0; m<N_2C; m++ )
		fprintf( out_count, "%5d\t", count12[l][m] );
	    fprintf( out_count, "\n" );}
	    
    // L1 - L3  Distribution
    if( atoi(argv[5]) == 4 )
 	for( l=0; l<N_2C; l++ ){
	    for( m=0; m<N_2C; m++ )
		fprintf( out_count, "%5d\t", count13[l][m] );
	    fprintf( out_count, "\n" );}
	
    fclose(out_count);	
    
    //=============================================================================================
    return 0;
}