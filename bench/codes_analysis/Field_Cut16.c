#include <stdio.h>
#include <stdlib.h>
#define FLOAT float

//Usage  Field_Cut.out <filename> <cut in x/y/z> <output filename> <coordinate section>

int main(int argc, char **argv)
{    
    FILE *in, *field;
    FLOAT *delta;
    char filename[100];
    
    int ii, jj;
        
    //Grid variables===============================================================================
    int dumb;
    char line[30];
    long long i;
    int n_x, n_y, n_z;
    int n_nodes;
    long long n_total;
    float dx, dy, dz, x_0, y_0, z_0;
    //=============================================================================================
         
        
    //LOADING FIELD VALUES=========================================================================
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
    //fprintf(stderr, "Nx Ny Nz : %d %d %d %lld\n", n_x, n_y, n_z, n_total);
    //fprintf(stderr, "x_0 y_0 z_0 : %g %g %g\n", x_0, y_0, z_0);
    //fprintf(stderr, "dx dy dz : %g %g %g\n", dx, dy, dz);    
    
    if(!(delta=malloc(n_nodes * sizeof(FLOAT)))){
	fprintf(stderr, "problem with array allocation\n");
	exit(1);}
    fread(&dumb,sizeof(int),1,in);
    fread(&(delta[0]),sizeof(FLOAT), n_total, in);
    fread(&dumb,sizeof(int),1,in);
    
    fclose(in);

    
    //SAVING FIELD VALUES==========================================================================

    //New file for density field values
    sprintf(filename, "%s", argv[3]);
    field=fopen(filename, "w");

    // X Direction
    if ( atoi(argv[4]) == 1 ){    
	for( ii=0; ii<n_x; ii++ )
	    for( jj=0; jj<n_y; jj++ )
	      fprintf( field, "%1.6f\n", delta[ atoi(argv[2]) + n_x * (ii + n_y * jj ) ] );}
    
    // Y Direction
    if ( atoi(argv[4]) == 2 ){    
	for( ii=0; ii<n_x; ii++ )
	    for( jj=0; jj<n_y; jj++ )
	      fprintf( field, "%1.6f\n", delta[ ii + n_x * (atoi(argv[2]) + n_y * jj ) ] );}
    
    // Z Direction
    if ( atoi(argv[4]) == 3 ){    
	for( ii=0; ii<n_x; ii++ )
	    for( jj=0; jj<n_y; jj++ )
	      fprintf( field, "%1.6f\n", delta[ ii + n_x * (jj + n_y * atoi(argv[2]) ) ] );}

    fclose(field);

    //=============================================================================================
    return 0;
}
