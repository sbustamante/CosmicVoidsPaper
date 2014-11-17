#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MY_FREE(ptr)	free(ptr); ptr = NULL;

#define FLOAT1 float
#define FLOAT2 double
#define NMAX1 2000
#define NMAX2 30000
#define CELL2MPC 0.9765625

//Usage  Void_Density_Bins.out <delta_filename> <output_folder> <Void_Index> <CM> <Bins> <Rmax> <Rvmin> <Rvmax> <Nint>


/**************************************************************************************************
			      STRUCTURES
**************************************************************************************************/
struct void_region{
    int C[3];
    float R;
    float rho_mean;
    int Ncells;
    };

struct bins{
    long int Ncells;
    float Rint;
    double rho_median;
    double *rhos;
    };

/**************************************************************************************************
			      FUNCTIONS
**************************************************************************************************/
//Median of a list
float median( struct bins bin )
{
    long int i, j;
    int breaker;
    double dumb;
    
    for( j=0; j<bin.Ncells; j++ ){
	breaker = 0;	//False
	for( i=0; i<bin.Ncells-1; i++ ){
	    if( bin.rhos[i]>bin.rhos[i+1] ){
		dumb = bin.rhos[i];
		bin.rhos[i] = bin.rhos[i+1];
		bin.rhos[i+1] = dumb;
		breaker = 1;	//True
	    }
	}
	if( breaker == 0 ) break;
    }
  
    return bin.rhos[(int)(bin.Ncells/2.0)];
}

    

int main(int argc, char **argv)
{   
    FILE *in, *out;
    FLOAT2 *delta;
    FLOAT2 RC_mag;
    char filename[NMAX1];
    
    struct void_region voids[NMAX2];
    struct bins *rho_bins;
    
    int i,j,k;
    int ic,jc,kc;
    int it,jt,kt;
    int iv, ibin, itbin;
    long long int n, Ncells;
    
    //Grid variables===============================================================================
    int dumb;
    float dumbf;
    char line[30];
    int n_x, n_y, n_z;
    int n_nodes;
    long long n_total;
    float dx, dy, dz, x_0, y_0, z_0;
    //=============================================================================================
    
    //Loading centre and radius of void============================================================
    int Nbins, R, Nvoids, Rint, Nint;
    float Rvmin, Rvmax;
    Nbins = atoi( argv[5] );	//Number of radial bins
    R = atoi( argv[6] );	//Radius of void
    Rvmin = atof( argv[7] );	//Minimum bin radius for void stacking
    Rvmax = atof( argv[8] );	//Maximum bin radius for void stacking
    Nint = atoi( argv[9] );	//Number of intervals for void stacking
           	
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
    fclose( in );
    //=============================================================================================
    
    //LOADING VOIDS INDEXES========================================================================
    if(!(in=fopen(argv[3], "r"))){
	fprintf(stderr, "Problem opening file %s\n", argv[2]);
	exit(1);}
    
    //Reading and initializing voids
    i = 0;
    while( getc( in ) != EOF ){
	fscanf( in , "%d\t%f", &dumb, &voids[i].R );
	voids[i].R = pow( 3/(4.0*M_PI)*voids[i].R, 1/3.0 );
	voids[i].Ncells = 0;
	i++;}
	
    fclose( in );
    //=============================================================================================
    
    //LOADING VOIDS CM=============================================================================
    if(!(in=fopen(argv[4], "r"))){
	fprintf(stderr, "Problem opening file %s\n", argv[2]);
	exit(1);}
    
    //Reading
    i = 0;
    while( getc( in ) != EOF ){
	fscanf( in , "%d\t%f\t%f\t%f\t%d\t%d\t%d", &dumb, 
		&dumbf, &dumbf, &dumbf, 
		&voids[i].C[0], &voids[i].C[1], &voids[i].C[2] );
	i++;}
	
    Nvoids = i-1;
    fclose( in );
    //=============================================================================================

    //HISTOGRAMS===================================================================================
    rho_bins = (struct bins *)calloc( Nbins, sizeof( struct bins ) );
    //Reseting bins with normed radius and null cells
    for( i=0; i<Nbins; i++ ){
	rho_bins[i].Rint = 1.0*R*(i+1)/Nbins;
	rho_bins[i].Ncells = 1;
	rho_bins[i].rhos = (double *)calloc( rho_bins[i].Ncells, sizeof( double ) );
	rho_bins[i].rhos[0] = 0;
    }
 
    //SWEEPING VALUES
    itbin = Nint;
    
    out = fopen( "data", "w" );
    
    for( iv=0; iv<Nvoids; iv++ ){
	//If passing to the next bin
	if( voids[iv].R*CELL2MPC < Rvmin + (itbin-1)*(Rvmax-Rvmin)/Nint ){
	    fclose(out);
	    break;
	  
	    //Saving previous bin
// 	    printf( "\n\nSaving bins between effective radius [%f,%f]\n",
// 	    Rvmin + (itbin)*(Rvmax-Rvmin)/Nint,
// 	    Rvmin + (itbin-1)*(Rvmax-Rvmin)/Nint);

	    //Creating file to store density
	    sprintf( filename, "%s/density_%1.2f-%1.2f.dat", argv[2],
	    Rvmin + (itbin)*(Rvmax-Rvmin)/Nint,
	    Rvmin + (itbin-1)*(Rvmax-Rvmin)/Nint);
	    out = fopen( filename, "w" );
	    //Calculating medians
	    for( i=0; i<Nbins; i++ ){
// 		printf( "\tIn bin: %d\t\tNcells: %ld\n", i, rho_bins[i].Ncells );
// 		rho_bins[i].rho_median = median( rho_bins[i] );
		fprintf( out, "%1.5e\t%1.5e\n", rho_bins[i].Rint ,rho_bins[i].rho_median );
		//Reseting bins
		MY_FREE( rho_bins[i].rhos );
		rho_bins[i].Ncells = 1;
		rho_bins[i].rhos = (double *)calloc( rho_bins[i].Ncells, sizeof( double ) );
	    }
// 	    printf("\n");
	    fclose( out );
	    itbin --;}
		
	//Saving density field inside effecive radius of void
	Rint = (int)(voids[iv].R*R);
	for( i=voids[iv].C[0]-Rint; i<voids[iv].C[0]+Rint+1; i++ )
	for( j=voids[iv].C[1]-Rint; j<voids[iv].C[1]+Rint+1; j++ )
	for( k=voids[iv].C[2]-Rint; k<voids[iv].C[2]+Rint+1; k++ ){
	    it = i; jt = j; kt = k;
	    //Neighbor out of limits (Periodic boundary conditions) (X direction)
	    if( i>=n_x )	it -= n_x;
	    if( i<0 )		it += n_x;
	    //Neighbor out of limits (Periodic boundary conditions) (Y direction)
	    if( j>=n_x )	jt -= n_x;
	    if( j<0 )		jt += n_x;
	    //Neighbor out of limits (Periodic boundary conditions) (Z direction)
	    if( k>=n_x )	kt -= n_x;
	    if( k<0 )		kt += n_x;
	    
	    //Overall index
	    n = kt + n_x*(jt + n_x*it);
	    //Radial distance
	    RC_mag = sqrt( pow(voids[iv].C[0]-i,2) + pow(voids[iv].C[1]-j,2) + pow(voids[iv].C[2]-k,2) )/voids[iv].R;
	    ibin = (int)(RC_mag/R*Nbins);
	    //Only spherical bins
	    if( ibin < Nbins ){
		//Storing cells
		voids[iv].rho_mean += delta[n];
		voids[iv].Ncells ++ ;
		
		fprintf( out, "%1.5e\t%1.5e\n", RC_mag ,delta[n] );
		
		rho_bins[ibin].Ncells ++;
		rho_bins[ibin].rhos = (double *)realloc(rho_bins[ibin].rhos, \
		rho_bins[ibin].Ncells*sizeof( double ) );
		rho_bins[ibin].rhos[ rho_bins[ibin].Ncells-1 ] = delta[n];}}
		
	printf( "In void %d\t\t Mean density of the void = %e\n", iv, voids[iv].rho_mean/voids[iv].Ncells );}
    //=============================================================================================
    
    return 0;
}