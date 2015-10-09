# -*- coding: utf-8 -*-
# This file is part of the Sunrise Project

__author__ = 'Jaime García Villena <elgambitero@gmail.com>'
__copyright__ = 'Copyright (C) 2015-2016 Mundo Reader S.L.'
__license__ = 'GNU General Public License v2 http://www.gnu.org/licenses/gpl2.html'


import serial
import glob
import time

class mechComm():

    def __init__(self):
        self.myport='error'
        ports=[]
        for device in ['/dev/ttyAMA*','/dev/ttyACM*', '/dev/ttyUSB*', '/dev/tty.usb*', '/dev/tty.wchusb*',
                           '/dev/cu.*', '/dev/rfcomm*']:
            ports = ports + glob.glob(device)
        print(">>> Finding a valid GRBL controller board...")
        print(ports)
        for port in ports:
        #try:
            self.serial = serial.Serial(port, 115200, timeout=2)
            time.sleep(4)
            self.serial.flush()
            if self.serial.isOpen():
                print(">>> Found "+ port+ " open...")
                self._reset()
                self.version = self.getData()
                if self.version is not None:
                    print(self.version)
                    break
                '''
                if version == "Grbl 0.9j ['$' for help]":
                    self.myport=port
                    print(">>> Success!")
                    break
                    '''
            #else:
            #    self.serial.close()
        #except:
        #    pass
        if self.myport=='error':
            print(">>> Could not find GRBL controller")
        return

    def getData(self):
        if self.serial.isOpen():
            out = ''
            try:
                while self.serial.inWaiting() > 0:
                    out += self.serial.read(1)
                    if out != '':
                        return out
            except:
                return out

    def write(self,string):
        self.serial.write(string)

    def _reset(self):
        self.serial.setDTR(False)
        time.sleep(0.022)
        self.serial.flushInput()
        self.serial.flushOutput()
        self.serial.setDTR(True)
        #self.getData()