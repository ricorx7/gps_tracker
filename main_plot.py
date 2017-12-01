import serial
import sys
import glob
import pynmea2
import plot_data
import threading


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


def plot():
    """
    Plot the incoming GPS data.
    :return:
    """
    #plot_data.plot_lat_lon_data()
    plot_data.plot_distance_data()


def record_serial():
    """
    Record the incoming data to text file.
    This text file will be read to update the plot.
    :return:
    """

    # Open the serial port connection
    gps = serial.Serial("/dev/tty.usbserial-FTZ7HJUI", baudrate=19200)

    # Read the GPS
    while True:
        try:
            line = gps.readline()
            line = line.decode("utf-8")
            #print(line)
            data = str(line).split(",")
            if data[0] == "$GPRMC" or data[0] == "$GPGGA":
                nmea = pynmea2.parse(line)
                print("Lat: ", nmea.latitude)
                print("Lon: ", nmea.longitude)
                with open("gps_pts.txt", "a+") as pos:
                     pos.write("{},{},{}\n".format(nmea.latitude, nmea.longitude, nmea.timestamp))
        except Exception as err:
            print(err)


def main():
    # Print all the available serial ports
    print("*** Serial Ports Available ***")
    for serial_port in list_serial_ports():
        print(serial_port)
    print("*****************************")

    # Monitor the serial port
    t = threading.Thread(target=record_serial)
    t.start()

    # Start plotting the data
    plot()


if __name__ == "__main__":
    main()



