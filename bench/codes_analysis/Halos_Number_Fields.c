#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define NMAX1		1000
#define MAXHALOS	500000
#define NBOX		256

//Usage  Halos_Number_Fields.out <halos_catalogue_filename>

struct halo{
    //Positions
    float r[3];
    //Velocities
    float v[3];
    //Mass
    float Mass;
    //Id
    int id;
    //Id of original file
    int id_or;
    };

    
/**************************************************************************************************
 NAME:       data_in
 FUNCTION:   read input file with masses, positions, velocities, id, ...
 INPUTS:     'halo' structure, input file name
 RETURN:     Number of data (rows)
**************************************************************************************************/
int data_in( struct halo halos[],
	     char filename[] )
{
    int i=0, j=0, Ndats;
    char cmd[100], filenamedump[100];
    FILE *file;
    float tmp;
    

    //File Detection
    file = fopen( filename, "r" );
    if( file==NULL ){
	printf( "  * The file '%s' don't exist!\n", filename );}
    fclose(file);

    //Conversed to plain text
    in2dump( filename );
    sprintf( filenamedump, "%s.dump", filename );
    file = fopen( filenamedump, "r" );
    
    //Read data
    while( getc( file ) != EOF ){
	fscanf( file,"%d %f %f %f %f %f %f %f %f %f %f %f %f %f", 
		&halos[i].id_or, 
		&halos[i].r[X], &halos[i].r[Y], &halos[i].r[Z],
		&halos[i].v[X], &halos[i].v[Y], &halos[i].v[Z],
		&tmp, 	&halos[i].Mass, &tmp, &tmp, &tmp, &tmp, &tmp );
	halos[i].id = i;
	i++;}

    //Number of rows in datafile
    Ndats = i-1;
    
    fclose( file );

    printf( "  * The file '%s' has been loaded!\n", filename );
    
    sprintf( cmd, "rm -rf %s.dump", filename );
    system( cmd );

    return Ndats;
}
    

int main(int argc, char **argv)
{   
    int *number;
    int i, Ndat;
    //Individual halos
    struct halo *halos;
    halos = (struct halo *)calloc( MAXHALOS, sizeof( struct halo ) );

    if(!(number=malloc( NBOX * NBOX * NBOX * sizeof(int)))){
	fprintf(stderr, "problem with array allocation\n");
	exit(1);}
	
    //Loading halos
    Ndat = data_in( halos, argv[1] )
    
	
    
    return 0;
}