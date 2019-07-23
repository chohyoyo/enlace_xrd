#%%
import os
import sys
import glob
import csv
import conlog_parse as cp

def collect_out(condir):
    retval = []
    for root, dirs, files in os.walk(condir): 
        for file in files:
            if file.endswith(".out"):
                out_path = os.path.join(root,file)
                retval.append(out_path)
            else:
                pass
    return retval

def xrdfragcp_args(rows): #input must be a list with lines from the output file
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
        retval.update({'rdsize':0,'reqs':0,'time':0,'url':'none'})
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

def parse_out(outfile):     
    retval = {}

    fl_handle = open(outfile, 'r')
    fl_data = fl_handle.readlines()
    fl_handle.close()

    arguments = xrdfragcp_args(fl_data)
    
    if fl_data == []:
        retval['empty']=True
        retval.update({'url':"none",'reqs':0,'reqsize':0,'total_time':0})
    else:
        retval['empty']=False
        retval['url'] = arguments['url']
        retval['reqs'] = arguments['reqs']
        retval['total_time'] = gettotaltime(fl_data)
        retval['reqsize'] = int(arguments['rdsize'])/(int(arguments['reqs']) * 1024 * 1024)
    return retval

def average_rate(dir):
    retval = []
    paths = collect_out(dir)
    for path in paths:
        reqs = int(parse_out(path)['reqs'])
        reqsize = parse_out(path)['reqsize']
        tot_size = float(reqsize*reqs)
        tot_time = float(parse_out(path)['total_time'])
        if tot_time != 0:
            tot_rate = tot_size/tot_time
            retval.append(tot_rate)
        else:
            pass
    average = sum(retval)/len(retval)
    return average

def collect_empty_files(runDir):
    paths = collect_out(runDir)
    empty_out = []
    for path in paths:
        if parse_out(path)['empty'] == True:
            empty_out.append(path)
        else:
            pass
    if empty_out == []:
        empty_out.append("No empty output files.")
    print(empty_out)
    return empty_out

def avg_hostfreq(log_path):
    parseddata = cp.parse_job_data(log_path)
    procdata = cp.data_rows_by_proc(parseddata)
    slothosts = cp.slothosts_to_eviction_counts(procdata)
        
    all_host_data = list(slothosts.values())
    rel_host_data = all_host_data[1:]

    number_hosted = [item[0] for item in rel_host_data]

    avg_host_freq = sum(number_hosted)/len(number_hosted)

    return avg_host_freq

def parse_by_con(testDir,con):
    path = testDir
    x = str(con)

    log_paths = glob.glob(path+"con_"+x+"_*.log")
    con_dirs = glob.glob(path+"concurrency_"+x+"_*/")
    
    rates = []
    host_freq = []
    empty_files = []

    for dir in con_dirs:
        avg_rate = average_rate(dir)
        rates.append(avg_rate)
        list_empty = collect_empty_files(dir)
        if list_empty == []:
            print("empty list")
            empty_files.append(0)
        else:
            empty_files.append(len(list_empty))
    for log_path in log_paths:
        host_freq.append(avg_hostfreq(log_path))

    rate = sum(rates)/len(rates)
    host = sum(host_freq)/len(host_freq)
    empty = sum(empty_files)
    
    data = [rate, host, empty]

    return data

#%%

testDir = sys.argv[1]
con_list = sys.argv[2:]
data_list = []

for con in con_list:
    con_data = parse_by_con(testDir, con)
    data_list.append([int(con)] + con_data)

print(data_list)

with open('parsed.csv','w+') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['concurrency','rates','hosted','failed'])
    for data in data_list:
        writer.writerow(data)
#%%s