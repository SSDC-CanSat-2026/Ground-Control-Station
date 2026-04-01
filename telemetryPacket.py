class TelemetryPacket:
    TEAM_ID = ""
    MISSION_TIME = ""
    PACKET_COUNT = ""
    MODE = ""
    STATE = ""
    ALTITUDE = ""
    TEMPERATURE = ""
    PRESSURE = ""
    VOLTAGE = ""
    CURRENT = ""
    GYRO_R = ""
    GYRO_P = ""
    GYRO_Y = ""
    ACCEL_R = ""
    ACCEL_P = ""
    ACCEL_Y = ""
    GPS_TIME = ""
    GPS_ALTITUDE = ""
    GPS_LATITUDE = ""
    GPS_LONGITUDE = ""
    GPS_SATS = ""
    CMD_ECHO = ""
    valid_packet = False

    def __init__(self, string):
        try:
            fields = string.split(",") 
            self.TEAM_ID = fields[0]
            self.MISSION_TIME = fields[1]
            self.PACKET_COUNT = fields[2]
            self.MODE = fields[3]
            self.STATE = fields[4]
            self.ALTITUDE = fields[5]
            self.TEMPERATURE = fields[6]
            self.PRESSURE = fields[7]
            self.VOLTAGE = fields[8]
            self.CURRENT = fields[9]
            self.GYRO_R = fields[10]
            self.GYRO_P = fields[11]
            self.GYRO_Y = fields[12]
            self.ACCEL_R = fields[13]
            self.ACCEL_P = fields[14]
            self.ACCEL_Y = fields[15]
            self.GPS_TIME = fields[16]
            self.GPS_ALTITUDE = fields[17]
            self.GPS_LATITUDE = fields[18]
            self.GPS_LONGITUDE = fields[19]
            self.GPS_SATS = fields[20]
            self.CMD_ECHO = fields[21]
            self.valid_packet = True
        except Exception as e:
            print("[Debug] Invalid Packet Initialization")
            return

    def get_str(self):
        if self.valid_packet:
            return f"{self.TEAM_ID},{self.MISSION_TIME},{self.PACKET_COUNT},{self.MODE},{self.STATE},{self.ALTITUDE},{self.TEMPERATURE},{self.PRESSURE},{self.VOLTAGE},{self.CURRENT},{self.GYRO_R},{self.GYRO_P},{self.GYRO_Y},{self.ACCEL_R},{self.ACCEL_P},{self.ACCEL_Y},{self.GPS_TIME},{self.GPS_ALTITUDE},{self.GPS_LATITUDE},{self.GPS_LONGITUDE},{self.GPS_SATS},{self.CMD_ECHO}"
        else:
            return None
