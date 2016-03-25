#!/usr/bin/env python
import sys
import subprocess
import re
import os
import signal
import time
import copy

import yaml

def get_single_row(source_string, what_to_find):
    res_start = source_string.find(what_to_find) + len(what_to_find)
    res_end = source_string.find('\n', res_start)
    return source_string[res_start:res_end]

def get_bench_total_rps(raw_result):
    bench_total_rps = get_single_row(raw_result, 'Requests/sec:')
    value = float(re.findall('\d+\.*\d+', bench_total_rps)[0])
    return value

def get_bench_avg_latency(raw_result):
    search_result = re.search('Latency\s+(\d+\.*\d+)ms', raw_result)
    #print("DEBUG: search_result is {}".format(search_result))
    avg_latency = None
    if search_result:
        avg_latency = float(search_result.groups(1)[0])
    return avg_latency


def run_command(cmd, shell=False):
    pid = subprocess.Popen(cmd, shell=shell)
    return pid



def run_service(config):
    print("INFO: running service...")
    cmd = config["service_cmd_line"]
    child = subprocess.Popen(cmd)
    return child

def stop_service(service_pid):
    print("INFO: stopping service...")
    os.kill(service_pid, signal.SIGKILL)

def run_wrk(config):
    cmd = config["wrk_cmd_line"]
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = child.communicate()
    if stderr:
        print("ERROR: wrk returns an error {}".format(stderr))
        sys.exit(1)

    return stdout        


def get_avg_metric(metric_list):
    metric_list_copy = copy.copy(metric_list)
    metric_list_copy.sort()
    return sum(metric_list_copy[1:-1])/(len(metric_list_copy) - 2)


def main():
    config = yaml.load(open(sys.argv[1]))

    service = run_service(config)
    time.sleep(config["warmup_time"])
    service_pid = service.pid
    rps_list = []
    latency_list = [] 
    try:
        for number in range(config["repeat_count"]):
            print("INFO: run wrk {}th time".format(number + 1))
            wrk_output = run_wrk(config)
            print("INFO: wrk_output is:\n {}".format(wrk_output))
            rps = get_bench_total_rps(wrk_output)
            rps_list.append(rps)
            avg_latency = get_bench_avg_latency(wrk_output)
            latency_list.append(avg_latency)
    finally:
        stop_service(service_pid)

    print("Average RPS: {}".format(get_avg_metric(rps_list)))
    print("Average Latency: {}".format(get_avg_metric(latency_list)))


if __name__ == "__main__":
    main()
