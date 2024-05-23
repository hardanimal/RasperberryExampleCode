# encoding: utf-8

__author__ = 'Danzel.Li'

import subprocess

# PARAMETERS
READ_CPU_COMMAND = "cat /sys/class/thermal/thermal_zone0/temp"

def read_cpu_temp():
    cmd = READ_CPU_COMMAND
    temp = _execute_cmd(cmd)
    return(float(temp) / 1000.00)

def _execute_cmd(cmd=""):
    cmds = cmd.split(" ")
    stdout = ""
    stderr = ""

    ps = subprocess.Popen(cmds, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = ps.communicate(timeout=90)
    if ps.returncode != 0 or stderr != b'':
        print("CMD result %s, error: %s" % (stdout, stderr))
        return(-99999)
    return(int(stdout))


if __name__ == "__main__":
    cpuTemp = read_cpu_temp()
    print(cpuTemp)
