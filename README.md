# enlace_xrd

### Introduction
The primary aim of this project is to conduct scale tests on the XRootD cache system using [GlideTester](https://github.com/ischeinkman/osgscal/tree/master/glideTester/doc).
This repository contains the executable file needed to run xrdfragcp and the code necessary to parse the standard output from the tests. The GlideTester and xrdfragcp files themselves, however, are not included.

### Running the Test

GlideTester is used to simulate simualtaneous data requests from multiple clients to the XRootD cache. This was done using two main scripts. The first, xrdfragcp, simulates individual client use by making requests to copy fragments of data from a given XRootD file URL. The second, frag-some.py, is a script that feeds a command to xrdfragcp with the appropriate arguments. This includes data fragment size, offset (of where the first downloaded block will start), download rate, and number of requests. It also ensures that the same file is not chosen by two clients by matching the jobID to a file in a list of file URLs.

Since frag-some.py already includes the command to call xrdfragcp, one only needs to run frag-some.py as the executable to be submitted by glideTester. To do so, first change the scripts permissions using the following command.

```
chmod +X frag-some.py
```

In glideTester's parameters.cfg file, set frag-some.py as the executable value (or if frag-some.py .

frag-some.py takes in six arguments. The first is the **path to the input file** 'all-files-ge-128.txt'. This is a list of 25995 lines file URLs that can be copied from. This is followed by the **offset, id, count, number of requests, and download rate in MB/10s** in that order.

```
executable=frag-some.py
arguments= ./input_files/all-files-ge-128M.txt 0 $(Process) 1 10 10

```
In this example, xrdfragcp will run with no offset, download each file once, make 10 requests per job, and download at a rate of 10MB/10s (that is, 1MB/s).

In the optional condor parameters, one must also transfer all input files. This includes frag-some.py, the input files folder included in the repository, and the compiled xrdfragcp executable. A new line is added for the Singularity image for xrdfragcp. The link is provided in the example below.

```
transfer_input_files=./frag-some.py,/opt/xrdfragcp,./UCSD-Tests/UCSD_Host-UCSD_Cache/input_files/
+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el7:latest"

```


### Parsing Standard Output

AveragePlots.py will need the matplotlib and pandas libraries. If these libraries are not present, the csv file should be copied and plots should be generated on another server that has the necessary packages installed.
{: .alert .alert-warning}

Collecting data from a run directory can be done with parse_out.py. To use this file, execute it as a python script with the run directory's path as the first argument followed by the concurrencies you would like it to collect data for. For example:

```
python parse/parse_out.py ~/enlace/run_20190719_144618/ 100 300 500  
```

The script will os.walk through the directory looking for all immediate subdirectories with the name 'con _ [concurrency]_ run _ [run number].log'. 

The script then writes a csv file containing information on the average rate, average number of jobs sent to each slot host, and the total number of failed jobs for each run of a given concurrency. It collects this information from both the standard output files of each job and also from the condor log files generated for each run.

AveragePlots.py can be used to then generate plots from the csv file. Running the python script with the csv file path passed as the first argument will generate and save .png images of the following plots:

* Average Rates per Concurrency
* Percent of Expected Rate Achieved per Concurrency
* Total Number of Failed Jobs per Concurrency (only if there were some jobs that failed. Otherwise, it just prints "No failed jobs")
* Average Number of Jobs Hosted per Host for concurrency

```
python parse/AveragePlots.py ~/enlace/parsed.csv
```



