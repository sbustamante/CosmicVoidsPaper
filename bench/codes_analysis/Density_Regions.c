#include <stdio.h>
#include <stdlib.h>
#define FLOAT1 float
#define FLOAT2 double
#define NMAX 1000

//USAGE  Density_Regions.out <EIG_Filename> <DELTA_Filename> <Min_Lambda> <Max_Lambda> <N_Lambda> <Out_Filename>

int main(int argc, char **argv)
{    
    FILE *in, *out_corr;
    FLOAT1 *eigen1, *eigen2, *eigen3;
    FLOAT2 *delta;
    FLOAT2 *sort_delta_v, *sort_delta_s, *sort_delta_f, *sort_delta_k;
    int *environment;
    char filename[100];
    
    FLOAT1 Lambda_min, Lambda_max, Lambda;
    int j, k, N_thr, eig;
    float Nrho[NMAX][4];
    float Nmed[NMAX][4];
    int Nreg[NMAX][4];
    
    //Grid variables===============================================================================
    int dumb;
    char line[30];
    long long i;
    long long i_v, i_s, i_f, i_k;
    int n_x, n_y, n_z;
    int n_nodes;
    long long n_total;
    float dx, dy, dz, x_0, y_0, z_0;
    //=============================================================================================
    
   
    //PARAMETERS===================================================================================
    //Number of divisions in Lambda_th array
    N_thr = atoi( argv[5] );     
    //Minim Lambda_th
    Lambda_min = atof( argv[3] );
    //Maxim Lambda_th
    Lambda_max = atof( argv[4] );
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
	fprintf(stderr, "dx dy dz : %g %g %g\n", dx, dy, dz);   */ 
	
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
/*    fprintf(stderr, "Nx Ny Nz : %d %d %d %lld\n", n_x, n_y, n_z, n_total);
    fprintf(stderr, "x_0 y_0 z_0 : %g %g %g\n", x_0, y_0, z_0);
    fprintf(stderr, "dx dy dz : %g %g %g\n", dx, dy, dz); */   
    
    //Loading densities
    if(!(delta=malloc(n_nodes * sizeof(FLOAT2)))){
	fprintf(stderr, "problem with array allocation\n");
	exit(1);}
    fread(&dumb,sizeof(int),1,in);
    fread(&(delta[0]),sizeof(FLOAT2), n_total, in);
    fread(&dumb,sizeof(int),1,in);
    
    //Allocating memory for densities in voids, sheets, filaments and knots
    if(!(sort_delta_v=malloc(n_nodes * sizeof(FLOAT2)))){
	fprintf(stderr, "problem with array allocation\n");
	exit(1);}
    if(!(sort_delta_s=malloc(n_nodes * sizeof(FLOAT2)))){
	fprintf(stderr, "problem with array allocation\n");
	exit(1);}
    if(!(sort_delta_f=malloc(n_nodes * sizeof(FLOAT2)))){
	fprintf(stderr, "problem with array allocation\n");
	exit(1);}
    if(!(sort_delta_k=malloc(n_nodes * sizeof(FLOAT2)))){
	fprintf(stderr, "problem with array allocation\n");
	exit(1);}
    
    fclose(in);

    //CORRELATIONS=================================================================================
    //Correlation File
    sprintf(filename, "%s", argv[6]);
    out_corr=fopen(filename, "w");

    //Initializing histograms
    for( j=0; j<N_thr; j++ )
	for( i=0; i<4; i++ ){
	    Nrho[j][i] = 0;
	    Nreg[j][i] = 0;}
    
    //Calculating mean and median densities and total volumes--------------------------------------
    for( j=0; j<N_thr; j++ ){
	
	//Initializing index for each density array according to each kind of region
	i_v = 0; i_s = 0; i_f = 0; i_k = 0;
	
	//Calculating mean densities and total volumes---------------------------------------------
	//Sweeping all the grid
	for( i=0; i<n_total; i++ ){
	    //Current Lambda
	    Lambda = Lambda_min + (Lambda_max - Lambda_min)*j/N_thr;
	    
	    //HISTOGRAMS
	    // voids
	    if( eigen1[i] <= Lambda && eigen2[i] <= Lambda && eigen3[i] <= Lambda ){
		Nreg[j][0] ++;
		Nrho[j][0] += delta[i];
		if( i_v == 0 ){
		    sort_delta_v[i_v] = delta[i];
		    i_v++;}
		else
		    if( delta[i]<sort_delta_v[i_v-1] ){
			sort_delta_v[i_v] = sort_delta_v[i_v-1];
			sort_delta_v[i_v-1] = delta[i];
			i_v++;}
		    else{
			sort_delta_v[i_v] = delta[i];
			i_v++;}}
	    // sheets    
	    if( eigen1[i] > Lambda && eigen2[i] <= Lambda && eigen3[i] <=  Lambda ){
		Nreg[j][1] ++;
		Nrho[j][1] += delta[i];
		if( i_s == 0 ){
		    sort_delta_s[i_s] = delta[i];
		    i_s++;}
		else
		    if( delta[i]<sort_delta_s[i_s-1] ){
			sort_delta_s[i_s] = sort_delta_s[i_s-1];
			sort_delta_s[i_s-1] = delta[i];
			i_s++;}
		    else{
			sort_delta_s[i_s] = delta[i];
			i_s++;}}		
	    // filaments    
	    if( eigen1[i] > Lambda && eigen2[i] >  Lambda && eigen3[i] <=  Lambda ){
		Nreg[j][2] ++;
		Nrho[j][2] += delta[i];
		if( i_f == 0 ){
		    sort_delta_f[i_f] = delta[i];
		    i_f++;}
		else
		    if( delta[i]<sort_delta_f[i_f-1] ){
			sort_delta_f[i_f] = sort_delta_f[i_f-1];
			sort_delta_f[i_f-1] = delta[i];
			i_f++;}
		    else{
			sort_delta_f[i_f] = delta[i];
			i_f++;}}
	    // knots
	    if( eigen1[i] >  Lambda && eigen2[i] >  Lambda && eigen3[i] >  Lambda ){
		Nreg[j][3] ++;
		Nrho[j][3] += delta[i];
		if( i_k == 0 ){
		    sort_delta_k[i_k] = delta[i];
		    i_k++;}
		else
		    if( delta[i]<sort_delta_k[i_k-1] ){
			sort_delta_k[i_k] = sort_delta_k[i_k-1];
			sort_delta_k[i_k-1] = delta[i];
			i_k++;}
		    else{
			sort_delta_k[i_k] = delta[i];
			i_k++;}}}

	//Calculating mean densities and total volumes---------------------------------------------
	// voids
	Nmed[j][0] = sort_delta_v[ (int)(Nreg[j][0]/2.0) ];
	// sheets
	Nmed[j][1] = sort_delta_s[ (int)(Nreg[j][1]/2.0) ];
	// filaments
	Nmed[j][2] = sort_delta_f[ (int)(Nreg[j][2]/2.0) ];
	// knots
	Nmed[j][3] = sort_delta_k[ (int)(Nreg[j][3]/2.0) ];
    }
    
    //File Head
    fprintf( out_corr, "#Lamb\t\tDrg1\t\tDrg2\t\tDrg3\t\tDrg4\t\tN1\t\tN2\t\tN3\t\tN4\t\tNtot\t\tMed1\t\tMed2\t\tMed3\t\tMed4\n");
    for( j=0; j<N_thr; j++ ){
      	//Current Lambda
	Lambda = Lambda_min + (Lambda_max - Lambda_min)*j/N_thr;
	
	fprintf( out_corr, "%1.3f\t%1.5e\t%1.5e\t%1.5e\t%1.5e\t%8d\t%8d\t%8d\t%8d\t%8d\t%1.5e\t%1.5e\t%1.5e\t%1.5e\n", Lambda, \
        Nrho[j][0], Nrho[j][1], Nrho[j][2], Nrho[j][3],
	Nreg[j][0], Nreg[j][1], Nreg[j][2], Nreg[j][3],
	Nreg[j][0] + Nreg[j][1] + Nreg[j][2] + Nreg[j][3],
	Nmed[j][0], Nmed[j][1], Nmed[j][2], Nmed[j][3]);}
	
    fclose(out_corr);	
    
    //=============================================================================================
    return 0;
}