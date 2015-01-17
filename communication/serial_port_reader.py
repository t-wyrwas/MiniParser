__author__ = 'twyrwas'
import serial
import time
import wx

class SerialPortReader:

    def __init__(self, container):
        self._container = container
        self._run = False
        self._serial = None
        self._config_data = {
            'port': 'COM2',
            'baudrate': 115200,
            'parity': serial.PARITY_NONE,
            'stopbits': serial.STOPBITS_ONE,
            'bytesize': serial.EIGHTBITS
        }

    def run(self):
        try:
            self._serial = serial.Serial(**self._config_data)
            if self._serial.isOpen():
                self._serial.close()
            self._serial.setTimeout(0.2)
            self._serial.open()
        except serial.SerialException, e:
            dlg = wx.MessageDialog(None, str(e), "Serial Port Error", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            self._run = True
            while True:
                if self._run == False:
                    break
                log = self._serial.readline()
                if log is not '':
                    self._container.append(log)

    def stop(self):
        if self._run is True:
            self._run = False
            self._serial.flushInput()
            self._serial.close()