#!/bin/bash
sudo lsmod | grep ftdi_sio
sudo rmmod ftdi_sio
sudo rmmod usbserial
/bin/python /home/bench2o/FluidController/BencH2O.py