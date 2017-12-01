import serial
import pynmea2
import threading
import Settings as Settings


def monitor(output_port):
    """
    Monitor the GPS port
    :param output_port: Output serial port to write data to.
    :return:
    """
    # Open the serial port connection
    serial_port = serial.Serial(Settings.GPS_PORT,               # Serial Port
                                baudrate=Settings.GPS_BAUD)      # Baud

    # Read the GPS
    while True:
        try:
            # Read the line from the serial port
            line = serial_port.readline()
            #print(line.decode("utf-8"))

            # Pass to output port
            output_port.write(line)

        except Exception as err:
            print("Gps Write output error. ", err)


def main():

    # Monitor the serial port
    t = threading.Thread(target=monitor)
    t.start()


if __name__ == "__main__":
    main()
