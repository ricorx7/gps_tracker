import serial
import sys
import glob
import threading
from OutputPort import OutputPort
import VectorNav
import Gps


def list_serial_ports():
    """ Lists serial port names

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of the serial ports available on the system
    """

    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except OSError as err:
            print(err)
            pass
        except Exception as err:
            print(err)
            pass
    return result


def output_all_data():
    """
    Create all the serial port connections.
    Take in the Vector Nav compass data.
    Take in the GPS data.
    Have the compass and GPS data output to OutputPort.
    :return:
    """
    # Create an output serial port to output all incoming data
    output_port = OutputPort()

    # Monitor Incoming Vector Nav data
    t_vn = threading.Thread(target=VectorNav.monitor, args=(output_port,))
    t_vn.start()

    # Monitor Incoming GPS data
    t_gps = threading.Thread(target=Gps.monitor, args=(output_port,))
    t_gps.start()


def main():
    # Print all the available serial ports
    print("*** Serial Ports Available ***")
    for serial_port in list_serial_ports():
        print(serial_port)
    print("*****************************")

    # Monitor for incoming data and output the data to new serial port
    t = threading.Thread(target=output_all_data)
    t.start()

if __name__ == "__main__":
    main()



