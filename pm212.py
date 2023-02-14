# encoding: utf-8

__author__ = 'Danzel.Li@ii-vi.com'

import time
import serial


class PortDoesNotExist(Exception):
    pass


class PortCanNotOpen(Exception):
    pass


class PM212(object):
    
    def __init__(self, port='/dev/ttyUSB0', baudrate=19200, **kvargs):
        timeout = kvargs.get('timeout', 1)
        parity = kvargs.get('parity', serial.PARITY_NONE)
        bytesize = kvargs.get('bytesize', serial.EIGHTBITS)
        stopbits = kvargs.get('stopbits', serial.STOPBITS_ONE)
        try:
            import os
            if not os.path.exists(port):
                raise PortDoesNotExist("Couldn't open serial port - serial port config error!")
            self.ser = serial.Serial(port=port, baudrate=baudrate,
                                     timeout=timeout, bytesize=bytesize,
                                     parity=parity, stopbits=stopbits)
        except PortCanNotOpen:
            raise PortCanNotOpen("Couldn't open serial port - PM212 does NOT exist!")

        if not self.ser.isOpen():
            self.ser.open()
            
        self._cleanbuffer_()
    

    def __del__(self):
        if 'ser' in locals().keys():
            self.ser.close()
        

    def _cleanbuffer_(self):
        self.ser.flushInput()
        self.ser.flushOutput()
        

    def reset(self):
        self._cleanbuffer_()
        self.ser.write(b'0')
        
        
    def get_serial_number(self):
        self._cleanbuffer_()
        self.ser.write(b'n')
        sRet = str(self.ser.readline(), encoding='ascii')
        return ""
        
        
    def get_wavelength(self):
        self._cleanbuffer_()
        self.ser.write(b'l')
        sRet = str(self.ser.readline(), encoding='ascii')
        return sRet
        
        
    def set_wavelength(self, dWavelength):
        if dWavelength == 850:
            nWavelength = 850
        elif dWavelength == 1310:
            nWavelength = 1310
        elif dWavelength >= 1270 and dWavelength <= 1340:
            nWavelength = 1300
        elif dWavelength >= 1470 and dWavelength <= 1520:
            nWavelength = 1490
        elif dWavelength >= 1521 and dWavelength <= 1590:
            nWavelength = 1550
        elif dWavelength >= 1591 and dWavelength <= 1625:
            nWavelength = 1625
        else:
            raise Exception("WAVELENGTH " + str(dWavelength) + " NOT SUPPORTED")
            
        retry = 0
        maxretry = 3
        
        for i in range(5):
            #read current wavelength
            self._cleanbuffer_()
            self.ser.write(b'l')
            time.sleep(0.25)
            sWavelength = str(self.ser.readline(), encoding='ascii').strip()
            
            if not sWavelength.isdigit():
                retry += 1
                if retry > maxretry:
                    raise Exception("MAX RETIES EXCEEDED TRYING TO SET WAVELENGTH")
                i -= 1
                continue

            if sWavelength == nWavelength:
                #wavelength is set correctly
                break

            #index to next wavelength
            self.ser.write(b'l')
        
        
    def get_power(self):
        dblPower = 0.0

        sPower = ""
        for i in range(5):

            self._cleanbuffer_()
            self.ser.write(b'v')
            time.sleep(0.25)

            sPower = str(self.ser.readline(), encoding='ascii')

            if (sPower != "") and ("LL." not in sPower) and ("NaN" not in sPower):
                break
            else:
                sPower = "-999.0"

        dblPower = float(sPower)

        if dblPower <= -100:
            dblPower = -80.0

        return dblPower
        
    

if __name__ == "__main__":
    pm212 = PM212()
    pm212.reset()
    print(pm212.get_serial_number())
    print(pm212.get_wavelength())
    pm212.set_wavelength(1550)
    print(pm212.get_power())

