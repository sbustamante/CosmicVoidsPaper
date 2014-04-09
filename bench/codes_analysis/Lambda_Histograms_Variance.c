#include <stdio.h>
#include <stdlib.h>
#define FLOAT1 float
#define NMAX1 100
#define NMAX2 1000

//Usage  Lambda_Histograms_Variance.out 
//   	 <eig_filename> <size of 1D hist> <Lambda range> <N_div> <Histogram Type>
// Histogram Type
//	0	L1
//	1	L2
//	2	L3

int main(int argc, char **argv)
{   
    FILE *in, *out_count;
    FLOAT1 *eigen1, *eigen2, *eigen3;
    char filename[100];
    float Lambda_ex, L1, L2, L3;
    
    int l, m, n, N_1C, eig;
    int ii, jj, kk, octx, octy, octz, oct_id, N_div;
    int countL1[NMAX2][NMAX1], countL2[NMAX2][NMAX1], countL3[NMAX2][NMAX1];

    
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
    //Number of divisions of simulation
    N_div = atoi( argv[4] );     
    //Number of divisions in Lambda count
    N_1C = atoi( argv[2] );     
    //Lambdas Range
    Lambda_ex = atof( argv[3] );
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

    //Initializing counts
    for( l=0; l<N_1C; l++ )
	for( m=0; m<N_div; m++ ){
	    countL1[l][m] = 0;
	    countL2[l][m] = 0;
	    countL3[l][m] = 0;}
    
                    
    //Building the histograms of eigenvalues counts
    oct_id = 0;
    for( octx=0; octx<N_div; octx++ )
    for( octy=0; octy<N_div; octy++ )
    for( octz=0; octz<N_div; octz++ ){
	  
	for( ii=(int)(n_x*octx/N_div); ii<(int)(n_x*(octx+1)/N_div); ii++ )
	for( jj=(int)(n_y*octy/N_div); jj<(int)(n_y*(octy+1)/N_div); jj++ )
	for( kk=(int)(n_z*octz/N_div); kk<(int)(n_z*(octz+1)/N_div); kk++ ){
	if( fabs(eigen1[i])<Lambda_ex || fabs(eigen3[i])<Lambda_ex ){
	    i = ii + n_x * (jj + n_y * kk );
	    
	    //1D Histograms
	    l = (int)( N_1C*(eigen1[i] + Lambda_ex)/(2*Lambda_ex) );
	    m = (int)( N_1C*(eigen2[i] + Lambda_ex)/(2*Lambda_ex) );
	    n = (int)( N_1C*(eigen3[i] + Lambda_ex)/(2*Lambda_ex) );

	    countL1[l][oct_id] ++ ;
	    countL2[m][oct_id] ++ ;
	    countL3[n][oct_id] ++ ;
	    	    
	}}
	oct_id ++;}

    // L1 Distribution
    if( atoi(argv[5]) == 0 )
      	for( l=0; l<N_1C; l++ ){
	    L1 = -Lambda_ex + ( 2*Lambda_ex )*l/N_1C;
	    fprintf( out_count, "%1.3e\t", L1 );
	    
	    for( oct_id=0; oct_id<N_div*N_div*N_div; oct_id++ )
		fprintf( out_count, "%d\t", countL1[l][oct_id] );
		
	    fprintf( out_count, "\n" );}
	  
	  
    // L2 Distribution
    if( atoi(argv[5]) == 1 )
      	for( l=0; l<N_1C; l++ ){
	    L2 = -Lambda_ex + ( 2*Lambda_ex )*l/N_1C;
	    fprintf( out_count, "%1.3e\t", L2 );
	    
	    for( oct_id=0; oct_id<N_div*N_div*N_div; oct_id++ )
		fprintf( out_count, "%d\t", countL2[l][oct_id] );
		
	    fprintf( out_count, "\n" );}
	  
	  
    // L2 Distribution
    if( atoi(argv[5]) == 2 )
      	for( l=0; l<N_1C; l++ ){
	    L3 = -Lambda_ex + ( 2*Lambda_ex )*l/N_1C;
	    fprintf( out_count, "%1.3e\t", L3 );
	    
	    for( oct_id=0; oct_id<N_div*N_div*N_div; oct_id++ )
		fprintf( out_count, "%d\t", countL3[l][oct_id] );
		
	    fprintf( out_count, "\n" );}

	
    fclose(out_count);	
    
    //=============================================================================================
    return 0;
}