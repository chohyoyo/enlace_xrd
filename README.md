# enlace_xrd

### Introduction
The primary aim of this project is to conduct scale tests on the XRootD cache system using glideTester. This repository contains the executable file needed to execute xrdfragcp and the code necessary to parse the standard output from the tests. However, the glideTester and xrdfragcp files themselves are not included.

### Running the Test

All tests were run using glideTester and formatted from glideTester's parameters file.

First, make frag-some.py executable with the command

```
chmod 777 frag-some.py
```
frag-some.py takes in six arguments. The first is the path to the input file 'all-files-ge-128.txt'. This is a list of 25995 lines file URLs that can be copied from. This is followed by the **offset, id, count, number of requests, and download rate in MB/10s** in that order.

*Offset refers to the block offset in the fragment to be retrieved (default value is 0). 
*ID is the job ID (set to $(Process)). 
*Count is the number of times the fragment will be downloaded
*requests is the total number of requests to be made by a single job.

Xrdfragcp must be run from within a singularity image whose link is printed below.

To start a run using xrdfragcp, set the path to frag-some.py as the value for glideTester's parameters and pass the appropriate arguments. For instance:

```
executable=frag-some.py
arguments= ./input_files/all-files-ge-128M.txt 0 $(Process) 1 10 10
+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el7:latest"

```
In this example, xrdfragcp will run with no offset, download each file once, make 10 requests per job, and download at a rate of 10MB/10s (that is, 1MB/s).

In the optional condor parameters, one must also transfer all input files. This includes frag-some.py, the input files folder included in the repository, and the compiled xrdfragcp executable.

```
transfer_input_files=./frag-some.py,/opt/xrdfragcp,./UCSD-Tests/UCSD_Host-UCSD_Cache/input_files/

```

Set the appropriate concurrencies and run number, and run with the command 

### Parsing Standard Output

Collecting data from a run directory can be done with parse_out.py. To use this file, execute it as a python script and give the run directory's path as the first argument followed by the concurrencies you would like it to collect data for. For example:
```
python parse/parse_out.py ~/enlace/run_20190719_144618/ 100 300 500  
```

This script requires all directories to be parsed to be immediate subdirectories of the directory that is passed as its argument. Running this script will also need to import the conlog_parse.py module.

The script then writes a csv file containing information on the average rate, average number of jobs sent to each slot host, and the total number of failed jobs for each run of a given concurrency. It collects this information from both the standard output files of each job and also from the condor log files generated for each run.

AveragePlots.py can be used to then generate plots from the csv file. Running the python script as an executable with the csv file path passed as the first argument will generate and save .png files of plots for the average rate per concurrency, average number of jobs per host for each concurrency, and the total number of failed jobs for all runs of a given concurrency. It also generates plots for the percent rate of achieved rate vs the expected rate.

AveragePlots.py will need the matplotlib and pandas libraries. If these libraries are not present (such as in test-001), the csv file can be copied to another server that has the necessary packages installed.
