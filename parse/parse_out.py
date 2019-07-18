#%%

import os
import sys


#returns a list of all output file paths in a given run's directory
def collect_out(rundir):
    retval = []
    for root, dirs, files in os.walk(rundir): 
        for file in files:
            if file.endswith(".out"):
                out_path = os.path.join(root,file)
                retval.append(out_path)
            else:
                pass
    return retval

def xrdfragcp_args(rows):
    retval = {}
     
    for row in rows:
        if 'Going to run' in row:
            cmdline = row
            cmdparts = []
            cmdparts = cmdline.split()

            retval.update({
                'rdsize':cmdparts[6],#the total requested size in bytes
                'reqs':cmdparts[7],#the number of requests it will make i.e. 10
                'time':cmdparts[8], #the calculated amount of time it will take
                'url':cmdparts[9]}) #the url the for the requested fragment
        else:
            pass
    if retval == {}:
        retval.update({'rdsize':'none','reqs':'none','time':'none','url':'none'})
    return retval

def gettotaltime(lines):
    beg = 0
    end = 0
    for line in lines:
        if "Start time:" in line:
            beg = float(line.split()[2])
        elif "End time:" in line:
            end = float(line.split()[2])
        else:
            pass
    time = end - beg
    if time == 0:
        print("no start or end time given")
    else:
        pass
    return time

def calcrate(lines,size):
    rates=[]
    for line in lines:
        if "Sleeping" in line:
            slptime = float(line.split()[2])
            time = 10 - slptime
            if time <= 0:
                time = 0.05
            rate = size/time #MB/s
            rates.append(rate)
        if "Not Sleeping" in line:
            time = 10 + float(line.split()[5])
            rate = size/time
            rates.append(rate)
        else:
            pass
    if len(rates)==0:
        print("No rate data available for this file")
        real_avgrate = 0
    else:
        real_avgrate = sum(rates)/len(rates)
    return real_avgrate
  
#listsamp = ['\n', 'total 128K\n', 'drwx------.  4 nobody nobody 4.0K Jul 16 10:23 .\n', 'drwxr-xr-x. 26 nobody nobody  760 Jul 16 10:23 ..\n', '-rwx------.  1 nobody nobody   48 Jul 16 10:23 .chirp.config\n', 'drwxr-xr-x.  2 nobody nobody 4.0K Jul 16 10:23 .gwms_aux\n', '-rw-r--r--.  1 nobody nobody 5.4K Jul 16 10:23 .job.ad\n', '-rw-r--r--.  1 nobody nobody  12K Jul 16 10:23 .machine.ad\n', '-rw-r--r--.  1 nobody nobody  11K Jul 16 10:23 .update.ad\n', '-rw-r--r--.  1 nobody nobody  446 Jul 16 10:23 _condor_stderr\n', '-rw-r--r--.  1 nobody nobody    1 Jul 16 10:23 _condor_stdout\n', '-rwxr-xr-x.  1 nobody nobody 2.0K Jul 16 10:23 condor_exec.exe\n', 'drwxrwxr-x.  2 nobody nobody 4.0K Jul 16 10:23 input_files\n', '-rw-------.  1 nobody nobody 9.7K Jul 16 10:23 pilot_proxy\n', '-rwxr-xr-x.  1 nobody nobody  53K Jul 16 10:23 xrdfragcp\n', 'frag-some.pl --- ./input_files/all-files-ge-128M.txt   0   2   1   10\n', '\n', 'Read 25995 lines from ././input_files/all-files-ge-128M.txt.\n', '\n', 'total 84K\n', '-rw-r--r--. 1 nobody nobody  446 Jul 16 10:23 _condor_stderr\n', '-rw-r--r--. 1 nobody nobody  896 Jul 16 10:23 _condor_stdout\n', '-rwxr-xr-x. 1 nobody nobody 2.0K Jul 16 10:23 condor_exec.exe\n', 'drwxrwxr-x. 2 nobody nobody 4.0K Jul 16 10:23 input_files\n', '-rw-------. 1 nobody nobody 9.7K Jul 16 10:23 pilot_proxy\n', '-rwxr-xr-x. 1 nobody nobody  53K Jul 16 10:23 xrdfragcp\n', '\n', 'Going to run ./xrdfragcp --verbose --cmsclientsim 209715200 10 100 root://xrootd.t2.ucsd.edu:2040//store/data/Run2016B/DoubleEG/MINIAOD/PromptReco-v1/000/272/776/00000/A410049A-FA15-E611-B9C6-02163E01352F.root.\n', '\n', '\n', 'Start time: 1563297832.05.\n', '\n', 'Starting CmsClientSim, 200.000000 MB to read in about 10 requests spaced by 10.0 seconds.\n', '  1 Reading 20.000 MB at offset 0\n', '    Sleeping for 9.7 seconds.\n', '  2 Reading 20.000 MB at offset 20971520\n', '    Sleeping for 9.8 seconds.\n', '  3 Reading 20.000 MB at offset 41943040\n', '    Sleeping for 9.8 seconds.\n', '  4 Reading 20.000 MB at offset 62914560\n', '    Sleeping for 9.8 seconds.\n', '  5 Reading 20.000 MB at offset 83886080\n', '    Sleeping for 9.8 seconds.\n', '  6 Reading 20.000 MB at offset 104857600\n', '    Sleeping for 9.8 seconds.\n', '  7 Reading 20.000 MB at offset 125829120\n', '    Sleeping for 9.7 seconds.\n', '  8 Reading 20.000 MB at offset 146800640\n', '    Sleeping for 9.7 seconds.\n', '  9 Reading 20.000 MB at offset 167772160\n', '    Sleeping for 9.7 seconds.\n', ' 10 Reading 20.000 MB at offset 188743680\n', '    Sleeping for 9.7 seconds.\n', '\n', 'Job ended.\n', '\n', '\n', 'End time: 1563297934.72.\n', '\n']
#calcrate(listsamp,20)

def parse_out(outfile):     
    retval = {}
    reqsize = 20 #size per request in MB
    retval['reqsize'] = reqsize
     
    fl_handle = open(outfile, 'r')
    fl_data = fl_handle.readlines()
    fl_handle.close()

    if fl_data == []:
        print("Error: Empty file: " + outfile)
        retval['url']="none"
        retval['real_avgrate']=0
        retval['reqs']= 0
        retval['total_time'] = 0
    else:
        arguments = xrdfragcp_args(fl_data)
        retval['url'] = arguments['url']
        retval['reqs'] = arguments['reqs']
        retval['real_avgrate'] = calcrate(fl_data,reqsize)
        retval['total_time'] = gettotaltime(fl_data)
    return retval


def collecturl(dir):
    retval = []
    paths = collect_out(dir)
    for path in paths:
        singleurl = parse_out(path)['url']
        retval.append(singleurl)
    return retval

def collectrates(dir):
    retval = {}
    paths = collect_out(dir)
    for path in paths:
        singlerate = parse_out(path)['real_avgrate']
        retval.update({path:singlerate})
    return retval
#get an average of the rates from collect rates. Output single value not array
def avgrate_everything(rundir):
    paths = collect_out(rundir)
    rates = []
    for path in paths:
        rate = parse_out(path)['real_avgrate']
        if not rate == 0:
            rates.append(rate)
        else:
            print("Removed data point")
    avg = sum(rates)/len(rates)
    return avg

#get the a list of rates using the start and end times printed on the output file
def collect_total_rates(rundir):
    retval = []
    paths = collect_out(rundir)
    for path in paths:
        reqs = float(parse_out(path)['reqs'])
        tot_size = float(parse_out(path)['reqsize']*reqs)
        tot_time = float(parse_out(path)['total_time'])
        if tot_time != 0:
            tot_rate = tot_size/tot_time
            retval.append(tot_rate)
        else:
            pass
    return retval






#%%
