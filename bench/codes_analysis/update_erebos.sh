#!/bin/bash

#Removing previous data ---------

rm ./BOLSHOI/Tweb/256/*
rm ./BOLSHOI/Tweb/512/*
rm ./BOLSHOI/Vweb/256/*
rm ./BOLSHOI/Vweb/512/*

rm ./CLUES/2710/Tweb/128/*
rm ./CLUES/2710/Vweb/128/*
rm ./CLUES/2710/Tweb/64/*
rm ./CLUES/2710/Vweb/64/*

rm ./CLUES/10909/Tweb/128/*
rm ./CLUES/10909/Vweb/128/*
rm ./CLUES/10909/Tweb/64/*
rm ./CLUES/10909/Vweb/64/*

rm ./CLUES/16953/Tweb/128/*
rm ./CLUES/16953/Vweb/128/*
rm ./CLUES/16953/Tweb/64/*
rm ./CLUES/16953/Vweb/64/*



#Updating the new data ----------

#BOLSHOI T-WEB-----------------------------------------------------------   
cp ../T-Web/Bolshoi/512/PMcrsFULL.0416.DAT.s1.00.eigen_1 ./BOLSHOI/Tweb/512/Eigen_s1_1
cp ../T-Web/Bolshoi/512/PMcrsFULL.0416.DAT.s1.00.eigen_2 ./BOLSHOI/Tweb/512/Eigen_s1_2
cp ../T-Web/Bolshoi/512/PMcrsFULL.0416.DAT.s1.00.eigen_3 ./BOLSHOI/Tweb/512/Eigen_s1_3

cp ../T-Web/Bolshoi/256/PMcrsFULL.0416.DAT.s1.00.eigen_1 ./BOLSHOI/Tweb/256/Eigen_s1_1
cp ../T-Web/Bolshoi/256/PMcrsFULL.0416.DAT.s1.00.eigen_2 ./BOLSHOI/Tweb/256/Eigen_s1_2
cp ../T-Web/Bolshoi/256/PMcrsFULL.0416.DAT.s1.00.eigen_3 ./BOLSHOI/Tweb/256/Eigen_s1_3

cp ../T-Web/Bolshoi/256/PMcrsFULL.0416.DAT.s1.00.DELTA ./BOLSHOI/Tweb/256/Delta_s1


#BOLSHOI V-WEB
cp ../V-Web/Bolshoi/512/PMcrsFULL.0416.DAT.s1.00.eigen_1 ./BOLSHOI/Vweb/512/Eigen_s1_1
cp ../V-Web/Bolshoi/512/PMcrsFULL.0416.DAT.s1.00.eigen_2 ./BOLSHOI/Vweb/512/Eigen_s1_2
cp ../V-Web/Bolshoi/512/PMcrsFULL.0416.DAT.s1.00.eigen_3 ./BOLSHOI/Vweb/512/Eigen_s1_3

cp ../V-Web/Bolshoi/256/PMcrsFULL.0416.DAT.s1.00.eigen_1 ./BOLSHOI/Vweb/256/Eigen_s1_1
cp ../V-Web/Bolshoi/256/PMcrsFULL.0416.DAT.s1.00.eigen_2 ./BOLSHOI/Vweb/256/Eigen_s1_2
cp ../V-Web/Bolshoi/256/PMcrsFULL.0416.DAT.s1.00.eigen_3 ./BOLSHOI/Vweb/256/Eigen_s1_3



#CLUES 2710 T-WEB-----------------------------------------------------------
cp ../T-Web/CLUES/WMAP5/2710/128/snap_191.s1.00.eigen_1 ./CLUES/2710/Tweb/128/Eigen_s1_1
cp ../T-Web/CLUES/WMAP5/2710/128/snap_191.s1.00.eigen_2 ./CLUES/2710/Tweb/128/Eigen_s1_2
cp ../T-Web/CLUES/WMAP5/2710/128/snap_191.s1.00.eigen_3 ./CLUES/2710/Tweb/128/Eigen_s1_3

cp ../T-Web/CLUES/WMAP5/2710/64/snap_191.s1.00.eigen_1 ./CLUES/2710/Tweb/64/Eigen_s1_1
cp ../T-Web/CLUES/WMAP5/2710/64/snap_191.s1.00.eigen_2 ./CLUES/2710/Tweb/64/Eigen_s1_2
cp ../T-Web/CLUES/WMAP5/2710/64/snap_191.s1.00.eigen_3 ./CLUES/2710/Tweb/64/Eigen_s1_3

cp ../T-Web/CLUES/WMAP5/2710/64/snap_191.s1.00.DELTA ./CLUES/2710/Tweb/64/Delta_s1


#CLUES 2710 V-WEB
cp ../V-Web/CLUES/WMAP5/2710/128/snap_191.s1.00.eigen_1 ./CLUES/2710/Vweb/128/Eigen_s1_1
cp ../V-Web/CLUES/WMAP5/2710/128/snap_191.s1.00.eigen_2 ./CLUES/2710/Vweb/128/Eigen_s1_2
cp ../V-Web/CLUES/WMAP5/2710/128/snap_191.s1.00.eigen_3 ./CLUES/2710/Vweb/128/Eigen_s1_3

cp ../V-Web/CLUES/WMAP5/2710/64/snap_191.s1.00.eigen_1 ./CLUES/2710/Vweb/64/Eigen_s1_1
cp ../V-Web/CLUES/WMAP5/2710/64/snap_191.s1.00.eigen_2 ./CLUES/2710/Vweb/64/Eigen_s1_2
cp ../V-Web/CLUES/WMAP5/2710/64/snap_191.s1.00.eigen_3 ./CLUES/2710/Vweb/64/Eigen_s1_3



#CLUES 10909 T-WEB-----------------------------------------------------------
cp ../T-Web/CLUES/WMAP5/10909/128/snap_190.s1.00.eigen_1 ./CLUES/10909/Tweb/128/Eigen_s1_1
cp ../T-Web/CLUES/WMAP5/10909/128/snap_190.s1.00.eigen_2 ./CLUES/10909/Tweb/128/Eigen_s1_2
cp ../T-Web/CLUES/WMAP5/10909/128/snap_190.s1.00.eigen_3 ./CLUES/10909/Tweb/128/Eigen_s1_3

cp ../T-Web/CLUES/WMAP5/10909/64/snap_190.s1.00.eigen_1 ./CLUES/10909/Tweb/64/Eigen_s1_1
cp ../T-Web/CLUES/WMAP5/10909/64/snap_190.s1.00.eigen_2 ./CLUES/10909/Tweb/64/Eigen_s1_2
cp ../T-Web/CLUES/WMAP5/10909/64/snap_190.s1.00.eigen_3 ./CLUES/10909/Tweb/64/Eigen_s1_3

cp ../T-Web/CLUES/WMAP5/10909/64/snap_190.s1.00.DELTA ./CLUES/10909/Tweb/64/Delta_s1


#CLUES 10909 V-WEB
cp ../V-Web/CLUES/WMAP5/10909/128/snap_190.s1.00.eigen_1 ./CLUES/10909/Vweb/128/Eigen_s1_1
cp ../V-Web/CLUES/WMAP5/10909/128/snap_190.s1.00.eigen_2 ./CLUES/10909/Vweb/128/Eigen_s1_2
cp ../V-Web/CLUES/WMAP5/10909/128/snap_190.s1.00.eigen_3 ./CLUES/10909/Vweb/128/Eigen_s1_3

cp ../V-Web/CLUES/WMAP5/10909/64/snap_190.s1.00.eigen_1 ./CLUES/10909/Vweb/64/Eigen_s1_1
cp ../V-Web/CLUES/WMAP5/10909/64/snap_190.s1.00.eigen_2 ./CLUES/10909/Vweb/64/Eigen_s1_2
cp ../V-Web/CLUES/WMAP5/10909/64/snap_190.s1.00.eigen_3 ./CLUES/10909/Vweb/64/Eigen_s1_3



#CLUES 16953 T-WEB-----------------------------------------------------------
cp ../T-Web/CLUES/WMAP5/16953/128/snap_190.s1.00.eigen_1 ./CLUES/16953/Tweb/128/Eigen_s1_1
cp ../T-Web/CLUES/WMAP5/16953/128/snap_190.s1.00.eigen_2 ./CLUES/16953/Tweb/128/Eigen_s1_2
cp ../T-Web/CLUES/WMAP5/16953/128/snap_190.s1.00.eigen_3 ./CLUES/16953/Tweb/128/Eigen_s1_3

cp ../T-Web/CLUES/WMAP5/16953/64/snap_190.s1.00.eigen_1 ./CLUES/16953/Tweb/64/Eigen_s1_1
cp ../T-Web/CLUES/WMAP5/16953/64/snap_190.s1.00.eigen_2 ./CLUES/16953/Tweb/64/Eigen_s1_2
cp ../T-Web/CLUES/WMAP5/16953/64/snap_190.s1.00.eigen_3 ./CLUES/16953/Tweb/64/Eigen_s1_3

cp ../T-Web/CLUES/WMAP5/16953/64/snap_190.s1.00.DELTA ./CLUES/16953/Tweb/64/Delta_s1


#CLUES 16953 V-WEB
cp ../V-Web/CLUES/WMAP5/16953/128/snap_190.s1.00.eigen_1 ./CLUES/16953/Vweb/128/Eigen_s1_1
cp ../V-Web/CLUES/WMAP5/16953/128/snap_190.s1.00.eigen_2 ./CLUES/16953/Vweb/128/Eigen_s1_2
cp ../V-Web/CLUES/WMAP5/16953/128/snap_190.s1.00.eigen_3 ./CLUES/16953/Vweb/128/Eigen_s1_3

cp ../V-Web/CLUES/WMAP5/16953/64/snap_190.s1.00.eigen_1 ./CLUES/16953/Vweb/64/Eigen_s1_1
cp ../V-Web/CLUES/WMAP5/16953/64/snap_190.s1.00.eigen_2 ./CLUES/16953/Vweb/64/Eigen_s1_2
cp ../V-Web/CLUES/WMAP5/16953/64/snap_190.s1.00.eigen_3 ./CLUES/16953/Vweb/64/Eigen_s1_3