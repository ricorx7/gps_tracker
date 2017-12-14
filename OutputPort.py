import serial
import socket
import Settings as Settings


class OutputPort:
    """
    Output all given data to the serial port.
    """

    def __init__(self):
        """
        Open the serial port.
        """
        # Open the serial port connection
        self.serial_port = serial.Serial(Settings.OUTPUT_PORT,               # Serial Port
                                         baudrate=Settings.OUTPUT_BAUD)      # Baud

        # Open the UDP port connection
        self.sock = socket.socket(socket.AF_INET,                            # Internet
                             socket.SOCK_DGRAM)                              # UDP

    def write(self, data):
        """
        Take incoming data and write it to the serial port.
        :param data: Data to write
        :return:
        """
        # Write the incoming data to the serial port
        self.serial_port.write(data)

        # Write the incoming data to the UDP port
        self.sock(data, (Settings.UDP_IP, Settings.UDP_PORT))
