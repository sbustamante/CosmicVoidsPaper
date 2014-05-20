#include <stdio.h>
#include <stdlib.h>

//Usage  Field_Cut_Plain.out <filename> <cut in x/y/z> <output filename> <coordinate section> <size of matrix>

int main(int argc, char **argv)
{
    int N;
    char filename[100];
    FILE *in, *out;
  
    //Grid variables===============================================================================
    int ii, jj;
    long long i;
    int *voids;
    //=============================================================================================
    
    
    //PARAMETERS===================================================================================
    //Size of matrix
    N = atoi( argv[5] );     
    voids = (int *)calloc( N*N*N, sizeof( int ) );
    //=============================================================================================

    
    //LOADING FIELD VALUES=========================================================================
    sprintf(filename, "%s", argv[1]);
    if(!(in=fopen(filename, "r"))){
	fprintf(stderr, "Problem opening file %s\n", filename);
	exit(1);}
    in = fopen( filename, "r" );
    if( in==NULL ){
	printf( "  * The file '%s' don't exist!\n", filename );}

    //Read data
    for( i=0; i<N*N*N; i++ )
	fscanf( in,"%d", &voids[i]);
    fclose( in );

    //Output data
    sprintf(filename, "%s", argv[3]);
    out = fopen( filename, "w" );

    // X Direction
    if ( atoi(argv[4]) == 1 ){
	for( ii=0; ii<N; ii++ )
	    for( jj=0; jj<N; jj++ )
	      fprintf( out, "%d\n", voids[ atoi(argv[2]) + N * (ii + N * jj ) ] );}

    // Y Direction
    if ( atoi(argv[4]) == 2 ){    
	for( ii=0; ii<N; ii++ )
	    for( jj=0; jj<N; jj++ )
	      fprintf( out, "%d\n", voids[ ii + N * (atoi(argv[2]) + N * jj ) ] );}
    
    // Z Direction
    if ( atoi(argv[4]) == 3 ){    
	for( ii=0; ii<N; ii++ )
	    for( jj=0; jj<N; jj++ )
	      fprintf( out, "%d\n", voids[ ii + N * (jj + N * atoi(argv[2]) ) ] );}
	      
    fclose( out );
    return 0;
}