# encoding: utf-8

__author__ = 'Danzel.Li@ii-vi.com'

import time
import pyvisa


device_addr = "TCPIP0::10.101.56.55::inst0::INSTR"
rm = pyvisa.ResourceManager("@py")
device_inst = rm.open_resource(device_addr)

print(device_inst.query("*IDN?"))

