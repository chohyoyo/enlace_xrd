# enlace_xrd

### Introduction
The primary aim of this project is to conduct scale tests on the XRootD cache system using glideTester. This repository contains the executable file needed to execute xrdfragcp and the code necessary to parse the standard output from the tests. GlideTester itself and xrdfragcp however are not included and may need to be found elsewhere.

### Running the Test
In glideTester's parameters, the executable file is frag-some.py. This script calls the program xrdfragcp and passes arguments to it.

### Parsing Standard Output

Collecting data from a run directory can be done with parse_out.py. To use this file, execute it as a python script and give the run directory's path as the first argument followed by the concurrencies you would like it to collect data for. For example:
> python parse/parse_out.py ~/enlace/run_20190719_144618/ 100 300 500  

This script requires that all directories to be parsed be immediate subdirectories of a single parent directory. Running this script will also require the conlog_parse.py module.

The script then writes a csv file containing information on the average rate, average number of jobs sent to each slot host, and the total number of failed jobs for each run of a given concurrency.

AveragePlots.py can be used to then generate plots from the csv file. Running the python script as an executable with the csv file path passed as the first argument will generate and save .png files of plots for the average rate per concurrency, average number of jobs per host for each concurrency, and the total number of failed jobs for all runs of a given concurrency. It also generates plots for the percent rate of achieved rate vs the expected rate.
