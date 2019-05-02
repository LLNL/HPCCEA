#!/usr/bin/python

import subprocess
import itertools
import time
import logging
import os
from multiprocessing import Process, Manager
from prometheus_client import start_http_server, Summary
from prometheus_client.core import GaugeMetricFamily, REGISTRY


try:
    TARGET_IPS="p4,p5,p6,p7,p8,p9,p10,p11"
    IPS = TARGET_IPS.split(',')
except AttributeError:
    raise Exception("Mandatory `TARGET_IPS` environment variable is not set")

IPMI_USER = os.getenv('IPMI_USER','root')
IPMI_PASSWD = os.getenv('IPMI_PASSWD','root')

REQURED = [
    "CPU1 Temp",
#    "CPU2 Temp",
    "CPU2 Temp",
    "Input Voltage",
    "Input Current"
]
# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


def _run_cmd(ip, raw):
    logging.info("Collecting from target %s", ip)
    proc = subprocess.Popen(["ipmitool",
                             "-H", ip,
                             "-U", IPMI_USER,
                             "-P", IPMI_PASSWD,
                             "sdr"], stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    #print out
    raw += [x.rstrip() for x in out.split('|')]


class IpmiCollector(object):
    @REQUEST_TIME.time()
    def collect(self):
        sys_metrics = {
            'cpu_temp1': GaugeMetricFamily('ipmi_cpu_temp1', 'CPU temp 1', labels=['ip']),
            'cpu_temp2': GaugeMetricFamily('ipmi_cpu_temp2', 'CPU temp 2', labels=['ip']),
            'sys_voltage': GaugeMetricFamily('ipmi_system_voltage', 'System Voltage', labels=['ip']),
            'sys_current': GaugeMetricFamily('ipmi_system_current', 'System Current', labels=['ip'])
        }
        raw = Manager().list([])
        for ip in IPS:
            # This is an attempt to run the `ipmi` tool in parallel
            # to avoid timeouts in Prometheus
            p = Process(target=_run_cmd, args=(ip, raw))
            logging.info("Start collecting the metrics")
            p.start()
            p.join()
            all_metrics = dict(itertools.izip_longest(*[iter(raw)] * 2, fillvalue=""))
            for k, v in all_metrics.items():
                for r in REQURED:
                    if r in k:
                        value = [float(s) for s in v.split() if s[0].isdigit()][0]
                        if 'CPU1' in k:
                            sys_metrics['cpu_temp1'].add_metric([ip], value)
                        elif 'CPU2' in k:
                            sys_metrics['cpu_temp2'].add_metric([ip], value)
                        elif 'Voltage' in k:
                            sys_metrics['sys_voltage'].add_metric([ip], value)
                        elif 'Current' in k:
                            sys_metrics['sys_current'].add_metric([ip], value)
                        else:
                            logging.error("Undefined metric: %s", k)

        for metric in sys_metrics.values():
            yield metric


def main():
    REGISTRY.register(IpmiCollector())
    start_http_server(8000)
    while True:
        time.sleep(5)

if __name__ == "__main__":
    logging.basicConfig(format='ts=%(asctime)s level=%(levelname)s msg=%(message)s', level=logging.DEBUG)
    main()
