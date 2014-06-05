#include <stdio.h>
#include <stdlib.h>
#define FLOAT1 float
#define FLOAT2 double
#define NMAX 5000

//USAGE  Density_Classification.out <DELTA_Filename> <N_div>

int main(int argc, char **argv)
{    
    FLOAT2 *delta, delta_sort;
    FILE *in, *out;
    char filename[100];
    
    int N_hist, i_n;
    double max_dens;
    float histogram[NMAX][2];
    
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
    //Number of divisions
    N_hist = atoi( argv[2] );
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
        
    fclose(in);

    //HISTOGRAM====================================================================================
    //Initial density
    max_dens = -1;
    //Finding maximum density
    for( i=0; i<n_total; i++ )
	if( delta[i] > max_dens )
	    max_dens = delta[i];

    //Initializing histogram
    for( i_n=0; i_n <= N_hist; i_n++ ){
	histogram[i_n][0] = -1 + i_n/(1.0*N_hist)*(max_dens + 1);
	histogram[i_n][1] = 0;}
	
    //Creating histograms
    for( i=0; i<n_total; i++ ){
	i_n = (int)( N_hist*(delta[i]+1)/(max_dens + 1) );
	histogram[i_n][1] ++;}    
	
    //File Head
    out = fopen( "temp.tmp", "w" );
    fprintf( out, "#\\delta\tNumber of cells\n");
    for( i_n=0; i_n <= N_hist; i_n++ )
	fprintf( out, "%1.5lf\t%lf\n", histogram[i_n][0], histogram[i_n][1] );
    fclose( out );
    
    //=============================================================================================
    return 0;
}