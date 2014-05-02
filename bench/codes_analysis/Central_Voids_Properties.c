#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define FLOAT1 float
#define FLOAT2 double
#define NMAX1 1000
#define NMAX2 100000

//Usage  Central_Voids_Properties.out <eig_filename> <delta_filename> <output_filename> <Number of neighbour cells>

float FractionalAnisotropy( float eig1, float eig2, float eig3 )
{ 
    float fa;
    fa = (1/pow(3,0.5))*pow( ( pow(eig1 - eig3,2) + pow(eig2 - eig3,2) + pow(eig1 - eig2,2) )/ \
    (eig1*eig1 + eig2*eig2 + eig3*eig3), 0.5 );
    return fa;
}

int main(int argc, char **argv)
{   
    FILE *in, *central_voids;
    FLOAT1 *eigen1, *eigen2, *eigen3, *FA;
    FLOAT2 *delta;
    char filename[100];
    int eig;
    
    int i,j,k,l;
    int ic,jc,kc;
    int it,jt,kt;
    int b = atoi( argv[4] );
    long long int n, nt;

    int isminim;
    
    //Grid variables===============================================================================
    int dumb;
    char line[30];
    int n_x, n_y, n_z;
    int n_nodes;
    long long n_total;
    float dx, dy, dz, x_0, y_0, z_0;
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

    //Allocating memory for FA
    if(!(FA=malloc(n_nodes * sizeof(FLOAT1)))){
	fprintf(stderr, "problem with array allocation\n");
	exit(1);}
	
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
    

    //FINDING LOCAL MINIMUM========================================================================
    for( i=0;i<n_x;i++ )
    for( j=0;j<n_x;j++ )
    for( k=0;k<n_x;k++ ){
	//Overall index
	n = k + n_x*(j + n_x*i);
	//Calculating FA
	FA[n] = FractionalAnisotropy( eigen1[n], eigen2[n], eigen3[n] );}
    
    //Open file
    sprintf( filename, "%s", argv[3] );
    central_voids = fopen(filename, "w");
    //Head
    fprintf( central_voids, "#i\tj\tk\tL1\tFA\tDelta\n" );
    
    for( i=0;i<n_x;i++ )
    for( j=0;j<n_x;j++ )
    for( k=0;k<n_x;k++ ){
	//Overall index
	n = k + n_x*(j + n_x*i);
	//Setting the neighborhood
	if( delta[n]<0 ){
	    //Setting this cell as a possible local minima
	    isminim = 1;
	    for( ic=-b; ic<=b; ic++ )
	    for( jc=-b; jc<=b; jc++ )
	    for( kc=-b; kc<=b; kc++ )
	    if( ic!=0 || jc!=0 || kc!=0 ){    
		it = i + ic; jt = j + jc; kt = k + kc;
		//Neighbor out of limits (Periodic boundary conditions) (X direction)
		if( i+ic>=n_x )		it = 0;
		if( i+ic<0 )		it = n_x-1;
		//Neighbor out of limits (Periodic boundary conditions) (Y direction)
		if( j+jc>=n_x )		jt = 0;
		if( j+jc<0 )		jt = n_x-1;
		//Neighbor out of limits (Periodic boundary conditions) (Z direction)
		if( k+kc>=n_x )		kt = 0;
		if( k+kc<0 )		kt = n_x-1;
		
		//Overall index of the neighbour
		nt = kt + n_x*(jt + n_x*it);
		
		if( FA[n] >= FA[nt] )
		    isminim = 0;}
	    if( isminim == 1 )
		fprintf( central_voids, "%d\t%d\t%d\t%1.5e\t%1.5e\t%1.5e\n", i,j,k,eigen1[n],FA[n],delta[n] );
	    }}
	
    fclose(central_voids);	
    //=============================================================================================
    return 0;
}