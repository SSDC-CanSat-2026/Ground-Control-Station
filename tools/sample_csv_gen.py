import csv
import pandas as pd
from datetime import datetime
import random
import numpy as np
import time
from datetime import datetime, timezone
import os

now = datetime.now()

state = "LAUNCH_WAIT"
mode = "S"
cmd = "CXON"
packet_count = 1
path = "./SimCSV.csv"
TEAM_ID = "1075"

fields = ["TEAM_ID","MISSION_TIME","PACKET_COUNT","MODE","STATE","ALTITUDE",
              "TEMPERATURE", "PRESSURE", "VOLTAGE","CURRENT",
              "GYRO_R", "GYRO_P", "GYRO_Y", "ACCEL_R", "ACCEL_P", "ACCEL_Y",
              "GPS_TIME", "GPS_ALTITUDE", "GPS_LATITUDE", "GPS_LONGITUDE", "GPS_SATS", "CMD_ECHO"]

df = pd.DataFrame(np.empty((0, len(fields))))

df.columns = fields

# There are 22 values sent in the telemetry packets, but the generated csv creates a 0th column with the
# number representing the current row, this causes the telemetry data to be effectively 1 indexed. I don't
# think this should be changed when the XBEE is implemented because it represents how many packets we have
# received not how many packets have been sent as is represented in the telemetry packet - Joel

df.loc[0] = [TEAM_ID, # Team_ID                                         1
            str(datetime.now())[11:][:-7], # Mission_Time               2
            packet_count, # Packet_Count                                3
            mode, # Mode                                                4
            state, # State                                              5
            random.randint(1,100), # Altitude                           6
            random.randint(1,100), # Temperature                        7
            random.randint(1, 100), # Pressure                          8
            random.randint(1, 100), # Voltage                           9
            random.randint(1, 100), # Current                           10
            random.randint(1,360), # Gyro_R                             11
            random.randint(1,360), # Gyro_P                             12
            random.randint(1,360), # Gyro_Y                             13
            random.randint(1,360), # Accel_R                            14
            random.randint(1,360), # Accel_P                            15
            random.randint(1,360), # Accel_Y                            16
            str(datetime.now())[11:][:-7], # GPS_Time                   17
            random.randint(1,100), # GPS_Altitude                       18
            random.randint(1, 50), # GPS_Latitude                       19
            random.randint(1, 50), # GPS_Longitude                      20
            random.randint(1, 3), # GPS_Sats                            21
            cmd] # CMD Echo                                             22

if not (os.path.exists(path)):
    df.to_csv(path, index=False)
else:
    packet_count = len(pd.read_csv(path))

global last_packet
last_packet = df.loc[0]
while(packet_count <= 1000):
    # print(f"Packet Count: {packet_count}")
    if packet_count % 25 == 0:
        time.sleep(10.0)
        print("Waiting for 10 seconds")

    if state == "LAUNCH_WAIT":
        state = "ASCENT"
    else:
        state = "LAUNCH_WAIT"

    if mode == "S":
        mode = "F"
    else:
        mode = "S"

    # if cmd == "CXON":
    #     cmd = "ST"
    # else:
    #     cmd = "CXON"
        
    if cmd == "SIMULATION ENABLE":
        cmd = "SIMULATION ACTIVATE"
    else:
        cmd = "SIMULATION ENABLE"

    packet_count += 1

    start = time.perf_counter()
    df.loc[0] = [   TEAM_ID, # Team_ID
                    datetime.now(timezone.utc).strftime('%H:%M:%S'), # Mission_Time in UTC
                    packet_count, # Packet_Count
                    mode, # Mode
                    state, # State
                    random.randint(1,100), # Altitude
                    random.randint(1,100), # Temperature
                    random.randint(1, 100), # Pressure
                    random.randint(1, 100), # Voltage
                    random.randint(1, 100), # Current
                    random.randint(1,360), # Gyro_R
                    random.randint(1,360), # Gyro_P
                    random.randint(1,360), # Gyro_Y
                    random.randint(1,360), # Accel_R
                    random.randint(1,360), # Accel_P
                    random.randint(1,360), # Accel_Y
                    str(datetime.now())[11:][:-7], # GPS_Time
                    df.iloc[-1]["GPS_ALTITUDE"] + random.randint(10,50), # GPS_Altitude
                    df.iloc[-1]["GPS_LATITUDE"] + random.randint(5,10), # GPS_Latitude
                    df.iloc[-1]["GPS_LONGITUDE"] + random.randint(1,5), # GPS_Longitude
                    random.randint(1, 3), # GPS_Sats
                    cmd] # CMD
    
    last_packet = df.loc[len(df.index)-1]
    time.sleep(0.5)

    df.to_csv(path, mode='a', header=False, index=False)
    end = time.perf_counter()
    duration = round(end - start, 5)
    print(f'Time to push data: {duration} seconds')


