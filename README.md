## main
Take in Vector Nav Compass data on one serial port.
Take in GPS data on one serial port.
Output all the incoming data to a serial port.

The Vector Nav data will be convert to a NMEA $GPHDT message.


## main_plot

Plot the GPS position

### INSTALL Notes
Windows 10 Bash

If you get an error about ImportError LibGL
```
sudo apt install libgl1-mesa-glx
sudo apt install python3-pyqt5
```