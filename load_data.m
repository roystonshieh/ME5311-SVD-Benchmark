clc; clear; close all

% dimensions of data
n_samples = 16071;
n_latitudes = 101; 
n_longitudes = 161;

% load data
ncfile = 'slp.nc'; % change to 't2m.nc' for temperature data

% visualize dataset content
ncinfo(ncfile)
ncdisp(ncfile)

% get 'slp'/'t2m' values
% 'msl' is the variable name for slp data, change to 't2m' for temperature data
x = ncread(ncfile, 'msl');

% get time snapshots
t = ncread(ncfile, 'time'); 

% get longitude values
lon = ncread(ncfile, 'longitude'); 

% get latitude values
lat = ncread(ncfile, 'latitude'); 