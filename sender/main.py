import json
import os
import sys
import time
from pathlib import Path

import psutil
import requests
from invoke import run


def blocking_stats():
    stats = {}
    p = psutil.Process()
    cmd_hdd = "{}/ioping.static -c10 -B -q -G -s100k -i0 .".format(os.path.dirname(os.path.realpath(__file__)))
    cmd_ram = "{}/ioping.static -c10 -B -q -G -s100k -i0 /tmp/".format(os.path.dirname(os.path.realpath(__file__)))
    cmd_process_count = "ps aux --no-heading"
    cnd_connection_count = "ss -s"
    stats["avg_cpu_15"] = os.getloadavg()[-1]
    stats["cpu_percent"] = psutil.cpu_percent(interval=None)
    stats["ram_percent"] = float("{0:.2f}".format(p.memory_percent() * 100))
    stats["hdd_iops"] = int(
        run(cmd_hdd, hide=True, warn=True).stdout.splitlines()[-1].split(" ")[2]
    )
    stats["ram_iops"] = int(
        run(cmd_ram, hide=True, warn=True).stdout.splitlines()[-1].split(" ")[2]
    )
    stats["proc_cnt"] = run(cmd_process_count, hide=True, warn=True).stdout.count("\n")
    stats["conn_cnt"] = int(
        run(cnd_connection_count, hide=True, warn=True)
        .stdout.splitlines()[0]
        .split(" ")[1]
    )
    return stats

if __name__ == "__main__":
    while True:
        # Path("/tmp/STAT").write_text(json.dumps(blocking_stats()))
        try:
            requests.post(sys.argv[1], json=blocking_stats())
        except Exception as e:
            print(e)
        time.sleep(2)
