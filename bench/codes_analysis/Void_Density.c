#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define FLOAT1 float
#define FLOAT2 double
#define NMAX1 1000

//Usage  Void_Density.out <delta_filename> <output_filename> <X> <Y> <Z> <R>


int main(int argc, char **argv)
{   
    FILE *in, *out;
    FLOAT2 *delta;
    char filename[NMAX1];
    int eig;
    
    int i,j,k;
    int ic,jc,kc;
    int it,jt,kt;
    long long int n;
    
    //Grid variables===============================================================================
    int dumb;
    char line[30];
    int n_x, n_y, n_z;
    int n_nodes;
    long long n_total;
    float dx, dy, dz, x_0, y_0, z_0;
    //=============================================================================================
    
    //Loading centre and radius of void============================================================
    int X, Y, Z, R;
    X = atoi( argv[3] );	//X coordinate
    Y = atoi( argv[4] );	//Y coordinate
    Z = atoi( argv[5] );	//Z coordinate
    R = atoi( argv[6] );	//Radius of void
    //=============================================================================================
           	
    //LOADING DENSITY FIELD========================================================================
    sprintf(filename, "%s", argv[1]);
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
    //=============================================================================================
    
    //Creating file to store density
    out=fopen(argv[2], "w");
    
    //Saving density field inside effecive radius of void
    for( i=X-R;i<X+R+1;i++ )
    for( j=Y-R;j<Y+R+1;j++ )
    for( k=Z-R;k<Z+R+1;k++ ){
	it = i; jt = j; kt = k;
	//Neighbor out of limits (Periodic boundary conditions) (X direction)
	if( i>=n_x )		it -= n_x;
	if( i<0 )		it += n_x;
	//Neighbor out of limits (Periodic boundary conditions) (Y direction)
	if( j>=n_x )		jt -= n_x;
	if( j<0 )		jt += n_x;
	//Neighbor out of limits (Periodic boundary conditions) (Z direction)
	if( k>=n_x )		kt -= n_x;
	if( k<0 )		kt += n_x;
	
	//Overall index
	n = kt + n_x*(jt + n_x*it);
	
	fprintf( out, "%d\t%d\t%d\t%1.5e\n", i,j,k,delta[n] );
    }
    
    fclose( out );
    
    return 0;
}