#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define FLOAT1 float
#define FLOAT2 double
#define NMAX1 2000
#define NMAX2 60000

//Usage  Void_Density_All.out <eig_filename> <output_folder> <Void_Index> <CM> <Bins> <Rmax>

/**************************************************************************************************
			      FUNCTIONS
**************************************************************************************************/
float FA( float eig1, float eig2, float eig3 )
{ 
    float fa;
    fa = (1/pow(3,0.5))*pow( ( pow(eig1 - eig3,2) + pow(eig2 - eig3,2) + pow(eig1 - eig2,2) )/ \
    (eig1*eig1 + eig2*eig2 + eig3*eig3), 0.5 );
    return fa;
}

/**************************************************************************************************
			      STRUCTURES
**************************************************************************************************/
struct void_region{
    int C[3];
    float R;
    };


int main(int argc, char **argv)
{   
    FILE *in, *out;
    FLOAT1 *eigen1, *eigen2, *eigen3;
    FLOAT1 RC_mag, fa_n;
    char filename[NMAX1];
    
    struct void_region voids[NMAX2];
    
    int i,j,k;
    int ic,jc,kc;
    int it,jt,kt;
    int iv, ibin;
    long long int n;
    
    //Grid variables===============================================================================
    int dumb, eig;
    float dumbf;
    char line[30];
    int n_x, n_y, n_z;
    int n_nodes;
    long long n_total;
    float dx, dy, dz, x_0, y_0, z_0;
    //=============================================================================================
    
    //Loading centre and radius of void============================================================
    int Nbins, R, Nvoids, Rint;
    Nbins = atoi( argv[5] );	//Number of radial bins
    R = atoi( argv[6] );	//Radius of void
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
    //=============================================================================================
    
    //LOADING VOIDS INDEXES========================================================================
    if(!(in=fopen(argv[3], "r"))){
	fprintf(stderr, "Problem opening file %s\n", argv[3]);
	exit(1);}
    
    //Reading
    i = 0;
    while( getc( in ) != EOF ){
	fscanf( in , "%d\t%f", &dumb, &voids[i].R );
	voids[i].R = pow( 3/(4.0*M_PI)*voids[i].R, 1/3.0 );
	i++;}
	
    fclose( in );
    //=============================================================================================
    
    //LOADING VOIDS CM=============================================================================
    if(!(in=fopen(argv[4], "r"))){
	fprintf(stderr, "Problem opening file %s\n", argv[4]);
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
     
 
    //Histograms
    float rho[NMAX1];
    int count[NMAX1];
    
    //Initializing histograms
    for( i=0; i<Nbins; i++ ){
	rho[i] = 0.0;
	count[i] = 0;}
    
    for( iv=0; iv<Nvoids; iv++ ){
	printf( "In void %d\n", iv );
	//Creating file to store density
	sprintf( filename, "%s/void_%d_FA.dat", argv[2], iv );
	out = fopen( filename, "w" );
	
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
	    //FA
	    fa_n = FA( eigen1[n], eigen2[n], eigen3[n] );
	    //Radial distance
	    RC_mag = sqrt( pow(voids[iv].C[0]-i,2) + pow(voids[iv].C[1]-j,2) + pow(voids[iv].C[2]-k,2) )/voids[iv].R;
	    ibin = (int)(RC_mag/R*Nbins);
	    rho[ibin] += fa_n+1;
	    count[ibin] ++;
	}

	//Initializing histograms
	for( i=0; i<Nbins; i++ ){
	    fprintf( out, "%1.5e\t%1.5e\n", 1.0*i*R/Nbins, rho[i]/count[i]-1 );
	    rho[i] = 0.0;
	    count[i] = 0;}
	
	fclose( out );
    
    }
    
    return 0;
}