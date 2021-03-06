from geopy.distance import vincenty
import Settings_tracker as settings
import serial
import pynmea2


class Tracker:
    """
    Track the GPS position and distance traveled.
    """

    def __init__(self):
        """
        Open the serial port.  Start tracking
        """
        self.first_pt = None

        # Open the serial port connection
        self.serial_port = serial.Serial(settings.TRACKER_PORT,               # Serial Port
                                         baudrate=settings.TRACKER_BAUD)      # Baud

        # Open file to record data
        self.file = open("gps_pts.txt", "a+", 128)                            # Set a small buffer size

        # Start tracking
        self.track()

    def track(self):
        """
        Read the serial port for GPS data.
        If the data contains GGA or RMC data, then decode it for Latitude and Longitude.
        Record the latitude and longitude to CSV file.
        Also display the distance traveled.
        :return:
        """

        while True:
            try:
                # Read the serial port
                line = self.serial_port.readline()

                # Convert data to UTF string
                line = line.decode("utf-8")
                # print(line)

                # Split the string by commas
                data = str(line).split(",")
                if data[0] == "$GPRMC" or data[0] == "$GPGGA":

                    # Parse the NMEA string
                    nmea = pynmea2.parse(line)
                    if self.first_pt:
                        print("First Pt: {}, {}".format(self.first_pt.latitude, self.first_pt.longitude))
                    print("Curr  Pt: {}, {}".format(nmea.latitude, nmea.longitude))

                    # Record positions
                    self.record_position(nmea)

                    # Calculate Distance traveled
                    self.calc_distanced_traveled(nmea)

            except Exception as err:
                print(err)

    def record_position(self, nmea):
        """
        Record the position to a file.
        :param nmea: NMEA data.
        :return:
        """
        self.file.write("{},{},{}\n".format(nmea.latitude, nmea.longitude, nmea.timestamp))

    def calc_distanced_traveled(self, nmea):
        """
        Calculate the distance traveled.
        :param nmea: NMEA data.
        :return:
        """
        if self.first_pt is None:
            # Store the first point
            self.first_pt = nmea
            print("FIRST POINT SET: {}, {}".format(self.first_pt.latitude, self.first_pt.longitude))
        else:
            # Calculate DMG
            first_pt = (self.first_pt.latitude, self.first_pt.longitude)
            curr_pt = (nmea.latitude, nmea.longitude)
            dmg = vincenty(first_pt, curr_pt).meters
            print("DMG: {} meters".format(dmg))
            print("--------------------------")