import serial
import pynmea2
import threading
import Settings as Settings


def monitor(output_port):
    """
    Monitor the Vector Nav Compass serial port.
    Decode there format and convert to an GPHDT format

    :param output_port: Output serial port to write data to.
    :return:
    """

    # Open the serial port connection
    serial_port = serial.Serial(Settings.VECTOR_NAV_PORT,               # Serial Port
                                baudrate=Settings.VECTOR_NAV_BAUD)      # Baud

    # Read the GPS
    while True:
        try:
            # Read the line from the serial port
            line = serial_port.readline()

            # Decode the line as a string
            # $VNYMR,-096.581,-001.050,+000.544,-00.1216,+00.2479,+00.6478,-00.180,-00.088,-09.385,+00.000818,-00.000947,-00.000141*6C\r\n'
            line = line.decode("utf-8")

            # Split the line to get the heading
            data = str(line).split(",")

            # Yaw is -180 to 180 so make 0 - 360
            heading = float(data[1]) + 180.0

            # Convert the Vector Nav message into a HDT message
            hdt = pynmea2.HDT('GP', 'HDT', ('{}'.format(heading), 'T'))
            #print(hdt)

            # Pass to output port
            output_port.write((str(hdt)+"\r\n").encode())

        except Exception as err:
            print("Vector Nav Write output error. ", err)


def main():

    # Monitor the serial port
    t = threading.Thread(target=monitor)
    t.start()


if __name__ == "__main__":
    main()
